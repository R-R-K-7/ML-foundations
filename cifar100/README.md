## Introduction 
* A model trained on CIFAR-100 dataset using Pytorch to classify images across diverse categories.

## Dependencies
* `torch`
* `torchvision`
* `matplotlib`

## Methodology
* Dataset - CIFAR100
* Architecture - A custom CNN architecture utilizing standard convolutional layers paired with ReLU activation functions for non-linear feature extraction.

## Observation & Results
* Accuracy on test dataset : 56.15% 
* Average loss on test dataset : 4.09
* While the accuracy seems modest, the dataset has high class variation with low resolution (32 x 32 x 3) images used.
