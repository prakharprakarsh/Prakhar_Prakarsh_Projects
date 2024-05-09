
clc;
% Loading the dataset
imageDir = '/Users/prakharprakarshgmail.com/Desktop/CNN classification/17flowers';

% Checking if the directorial existence
if exist(imageDir, 'dir') ~= 7
    error('The specified directory does not exist: %s', imageDir);
end

% Creating the image datastore
try
    imds = imageDatastore(imageDir, 'IncludeSubfolders', true, 'LabelSource', 'foldernames');
    fprintf('Number of images: %d\n', numel(imds.Files));
catch ME
    error('Error creating image datastore: %s', ME.message);

end

% Checking the number of unique class labels
uniqueLabels = unique(imds.Labels);
numClasses = numel(uniqueLabels);
fprintf('Number of classes: %d\n', numClasses);


% Reading the first image from the datastore
try
    img = readimage(imds, 1);
catch ME
    error('Error reading image from datastore: %s', ME.message);
end
% Displaying the image
try
    imshow(img);
catch ME
    error('Error displaying image: %s', ME.message);
end
% Data Preprocessing
imageSize = [256, 256];
imds.ReadFcn = @(filename)preprocessImage(filename, imageSize);

% Splitting the dataset into training and validation sets
[trainingImds, validationImds] = splitEachLabel(imds, 0.7, 'randomize');

% Data Augmentation
aug = imageDataAugmenter('RandRotation', [-20, 20]);
augmentedTrainingImds = augmentedImageDatastore(imageSize, trainingImds, 'ColorPreprocessing', 'gray2rgb', 'DataAugmentation', aug);
augmentedValidationImds = augmentedImageDatastore(imageSize, validationImds, 'ColorPreprocessing', 'gray2rgb', 'DataAugmentation', aug);

%Defining the CNN architecture

layers = [
    imageInputLayer([256 256 3])
    
    convolution2dLayer(3,8,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,16,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,32,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    fullyConnectedLayer(17)
    softmaxLayer
    classificationLayer];


%Defining training options


options = trainingOptions('sgdm', ... 
    'InitialLearnRate', 0.001, ... 
    'Momentum', 0.9, ... 
    'MaxEpochs', 34, ... 
    'MiniBatchSize', 32, ... 
    'Shuffle', 'every-epoch', ... 
    'ValidationData', augmentedValidationImds, ... 
    'ValidationFrequency', 10, ... 
    'Verbose', true, ... 
    'Plots', 'training-progress', ...
    'ExecutionEnvironment', 'auto');




% Training the CNN network
net = trainNetwork(augmentedTrainingImds, layers, options);

% Saving the trained network and class labels
save('classnet.mat', 'net');
save('classLabels.mat', 'uniqueLabels');

% Loading the saved network and class labels
load('classnet.mat');
load('classLabels.mat');

% Testing the  directory 
testImageDir = '/Users/prakharprakarshgmail.com/Desktop/CNN classification/17flowers_test';

% Creating an image datastore for test images
testImds = imageDatastore(testImageDir, 'IncludeSubfolders', true, 'LabelSource', 'foldernames');

% Preprocessing test images
testImds.ReadFcn = @(filename)preprocessImage(filename, imageSize);

% Classifying test images
predictedLabels = classify(net, testImds);

% Calculating classification accuracy
trueLabels = testImds.Labels;
accuracy = sum(predictedLabels == trueLabels) / numel(trueLabels);
fprintf('Test accuracy: %f\n', accuracy);


function img = preprocessImage(filename, imageSize)
    img = imread(filename);
    img = imresize(img, imageSize);
end










