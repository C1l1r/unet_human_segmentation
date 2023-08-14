# unet_human_segmentation
### General information
The goal of this project was to implement the UNET architecture from scratch and arrange model for use meeting all the modern industry standards.
## Data
The original dataset for this model was takken from kaggle and consists of images of humans. 

Link: https://huggingface.co/datasets/mattmdjaga/human_parsing_dataset/tree/main/data

## Model architecture

In this project was used the UNET model that consists of three parts: encoder, decoder and bottleneck.

## Training

The model was trained with the following specifications:

* OPTIMIZER = Adam
* LEARNING_RATE = 1e-4
* BATCH_SIZE = 32
* NUM_EPOCHS = 6
* LOSS FUNCTION = BCEWithLogitsLoss

## Dice Score
After training model achieved 96% dice score on validation dataset.

## Usage

To use the trained model for human segmentation, follow the instructions below:

Build docker image using command:

```
docker-compose -f docker_compose_file_path up
```
## Example:
```
docker-compose -f projects\human_segmentatiom\docker-compose.yml up
```
## Input and Output

