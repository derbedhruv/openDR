%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   image stitching Prototype
%   ------------------------------------------
%   Author: Chakri M
%
%   Take two images, slightly offset, and put features which are present
%   in both images to remove the "glare" portion from them and retain
%   original important image features.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


clc;
close all;
clear;

A = imread('1.jpg'); % Read first frame into imgA
B = imread('2.jpg'); % Read second frame into imgB

imgA = rgb2gray(A);
imgB = rgb2gray(B);

% figure; imshowpair(imgA, imgB, 'montage');
% title(['Frame A', repmat(' ',[1 70]), 'Frame B']);

%%
figure; imshowpair(imgA,imgB,'ColorChannels','red-cyan');
title('Color composite (frame A = red, frame B = cyan)');

%% Step 2. Collect Salient Points from each image
pointsA =  detectSURFFeatures(imgA);
pointsB =  detectSURFFeatures(imgB);

% Display corners found in images A and B.
% figure; imshow(imgA); hold on;
% plot(pointsA);
% title('Corners in A');

% figure; imshow(imgB); hold on;
% plot(pointsB);
% title('Corners in B');

%% 
[featuresA, pointsA] = extractFeatures(imgA, pointsA);
[featuresB, pointsB] = extractFeatures(imgB, pointsB);

%%
indexPairs = matchFeatures(featuresA, featuresB);
pointsA = pointsA(indexPairs(:, 1), :);
pointsB = pointsB(indexPairs(:, 2), :);

%%

%showMatchedFeatures(imgA, imgB, pointsA, pointsB);
% legend('A', 'B');

%% Step 4. Estimating Geometric Transform (Affine)

[tform, pointsBm, pointsAm] = estimateGeometricTransform(pointsB, pointsA, 'affine');
imgBp = imwarp(imgB, tform, 'OutputView', imref2d(size(imgB)));
pointsBmp = transformPointsForward(tform, pointsBm.Location);

%%

% showMatchedFeatures(imgA, imgBp, pointsAm, pointsBmp);
% legend('A', 'B');
% filling with minimum color values
% w1 = zeros(1944, 2592, 'uint8');

w1 = min(imgA, imgBp);

figure, clf;
imshow(w1);
title('Stitched Image (Final)');

