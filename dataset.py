from PIL import Image
import numpy as np
import os
from torch.utils.data import Dataset

# dataset = pd.read_parquet('data/train-00000-of-00002-9e861cba931f46ba.parquet')

# threshold = 1
# for i in range(0, int(0.9 * len(dataset['mask']))):
#     image_bytes = dataset['mask'][i]['bytes']
#     image = Image.open(io.BytesIO(image_bytes))
#     image = image.convert('L')
#     image = image.point(lambda p: p > threshold and 255)
#     image.save(f'data_png/train_masks/image_{i}_mask.png')
#     print(f'mask {i} saved')
#
#


class HumanData(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img_path = os.path.join(self.image_dir, self.images[index])
        mask_path = os.path.join(self.mask_dir, self.images[index].replace(".png", "_mask.png"))
        image = np.array(Image.open(img_path).convert("RGB"))
        mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
        mask[mask == 255.0] = 1.0

        if self.transform is not None:
            augmentations = self.transform(image=image, mask=mask)
            image = augmentations["image"]
            mask = augmentations["mask"]

        return image, mask