clc;
imagesFolder = '/Users/prakharprakarshgmail.com/Desktop/CNN Segmentation/daffodilSeg(segmentation)/ImagesRsz256';
labelFolder = '/Users/prakharprakarshgmail.com/Desktop/CNN Segmentation/daffodilSeg(segmentation)/LabelsRsz256';

% Defining the classes and labelIDs
classes = {'background', 'daffodil'};
labelIDs = [0, 1];

% Reading the image data
imagesFolder = '/Users/prakharprakarshgmail.com/Desktop/CNN Segmentation/daffodilSeg(segmentation)/ImagesRsz256';
imageDS = imageDatastore(fullfile(imagesFolder, '*.png'));

% Reading the image filenames
imgFiles = dir(fullfile(imagesFolder, '*.png'));
imgFileNames = {imgFiles.name}';

% Reading the label data
labelFiles = dir(fullfile(labelFolder, '*.png'));
labelFileNames = {labelFiles.name}';
pxLabelDS = pixelLabelDatastore(fullfile(labelFolder, labelFileNames), classes, labelIDs);

% Determining the number of files

numFiles = numel(imgFileNames);

% Determining the indices for training and validation sets

rng('default'); 
shuffledIndices = randperm(numFiles);
numTrain = round(0.8 * numFiles);
trainIndices = shuffledIndices(1:numTrain);
valIndices = shuffledIndices(numTrain+1:end);

% Splitting the data into training and validation sets

trainImgDatastore = imageDatastore(fullfile(imagesFolder, imgFileNames(trainIndices)));
valImgDatastore = imageDatastore(fullfile(imagesFolder, imgFileNames(valIndices)));
trainPxLabelDatastore = pixelLabelDatastore(fullfile(labelFolder, labelFileNames(trainIndices)), classes, labelIDs);
valPxLabelDatastore = pixelLabelDatastore(fullfile(labelFolder, labelFileNames(valIndices)), classes, labelIDs);

% Defining input size and number of classes

inputSize = [256, 256, 3];
numClasses = 2; % Background and daffodil classes

% Creating the UNet architecture using the function buildingUnet

lgraph = buildingUnet(inputSize, numClasses);

% Defining the training options for segmentation task

combinedValDatastore = combine(valImgDatastore, valPxLabelDatastore);
options = trainingOptions('adam', ...
    'MaxEpochs', 50, ... 
    'MiniBatchSize', 16, ...
    'InitialLearnRate', 1e-4, ...
    'Shuffle', 'every-epoch', ...
    'Verbose', true, ...
    'ValidationData', combinedValDatastore, ...
    'ValidationFrequency', 10, ...
    'ExecutionEnvironment', 'auto');

% Training the network to carry the operarions

combinedTrainDatastore = combine(trainImgDatastore, trainPxLabelDatastore);
net = trainNetwork(combinedTrainDatastore, lgraph, options);

% Predicting the labels for the validation set to work

valPred = semanticseg(valImgDatastore, net);

% Computing the metrics for evaluation of the model

metrics = evaluateSemanticSegmentation(valPred, valPxLabelDatastore, 'Verbose', true);


% visualisation the apparent results 

numValImages = numel(valImgDatastore.Files);
idx = randi(numValImages); 
I = readimage(valImgDatastore, idx);
C = readimage(valPxLabelDatastore, idx);
predictedCArray = cell(numValImages, 1);
for i = 1:numValImages
    I = readimage(valImgDatastore, i);
    predictedCArray{i} = semanticseg(I, net);
end
predictedC = predictedCArray{idx};
figure;
subplot(3, 1, 1);
imshow(I);
title('Original Image');
subplot(3, 1, 2);
imshow(labeloverlay(I, C, 'Transparency', 0.3));
title('Ground Truth');
subplot(3, 1, 3);
imshow(labeloverlay(I, predictedC, 'Transparency', 0.3));
title('Predicted Segmentation');

%Saving the training model

save('segmentnet.mat', 'net');

%Loading the saved model

load('segmentnet.mat');

%Testing the model on new images

testImagesFolder = '/Users/prakharprakarshgmail.com/Desktop/CNN Segmentation/daffodilSeg(segmentation)/Test images';
testImgDatastore = imageDatastore(fullfile(testImagesFolder, '*.png'));
numTestImages = numel(testImgDatastore.Files);
for i = 1:numTestImages

    %Testing the images

    testImage = readimage(testImgDatastore, i);

    % Resizing  the test images to match the input size of the network

    resizedTestImage = imresize(testImage, [256, 256]);

    % Performing semantic segmentation on the resized test images

    predictedLabels = semanticseg(resizedTestImage, net);

    % Visualising the segmentation results
 
     figure;
    subplot(2, 2, 1);
    imshow(resizedTestImage);
    title(sprintf('Test Image %d', i));

    subplot(2, 2, 2);
    imshow(labeloverlay(resizedTestImage, predictedLabels, 'Transparency', 0.3));
    title(sprintf('Predicted Segmentation %d', i));
end


%Defininig the CNN architecture

function lgraph = buildingUnet(inputSize, numClasses)
    encoder = [imageInputLayer(inputSize, 'Name', 'input'), ...
               convolution2dLayer(3, 64, 'Padding', 'same', 'Name', 'conv1_1'), ...
               reluLayer('Name', 'relu1_1'), ...
               maxPooling2dLayer(2, 'Stride', 2, 'Name', 'maxpool1')];
    middle = [convolution2dLayer(3, 128, 'Padding', 'same', 'Name', 'conv2_1'), ...
              reluLayer('Name', 'relu2_1')];
    decoder = [transposedConv2dLayer(2, 64, 'Stride', 2, 'Name', 'transConv1'), ...
               convolution2dLayer(3, numClasses, 'Padding', 'same', 'Name', 'conv3_1'), ...
               softmaxLayer('Name', 'softmax'), ...
               pixelClassificationLayer('Name', 'pixelLabels')];
    layers = [encoder, middle, decoder];
    lgraph = layerGraph(layers);

end

