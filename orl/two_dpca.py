import numpy as np

class TwoDPCA:
    def __init__(self, threshold=0.95):
        self.threshold = threshold
        self.projection_matrix = None

    def fit(self, images):
        image_shape = 60
        cov_matrix = np.zeros((image_shape, image_shape))
        for image in images:
            image = image.reshape(image_shape, image_shape)
            cov_matrix += np.dot(image.T, image)
        cov_matrix /= images.shape[0]

        eig_values, eig_vectors = np.linalg.eigh(cov_matrix)
        sorted_indices = np.argsort(eig_values)[::-1]
        eig_values = eig_values[sorted_indices]
        eig_vectors = eig_vectors[:, sorted_indices]

        cumulative_sum = np.cumsum(eig_values)
        total_sum = cumulative_sum[-1]
        num_components = np.searchsorted(cumulative_sum / total_sum, self.threshold) + 1

        self.projection_matrix = eig_vectors[:, :num_components]

    def transform(self, images):
        image_shape = 60
        projected_images = []
        for image in images:
            image = image.reshape(image_shape, image_shape)
            projected_image = np.dot(image, self.projection_matrix)
            projected_images.append(projected_image.flatten())
        return np.array(projected_images)

if __name__ == "__main__":
    from load_data import load_data
    from preprocess_data import preprocess_data

    data_dir = r'C:\Users\33455\Desktop\附加题\orl\archive'
    (train_images, train_labels), (test_images, test_labels) = load_data(data_dir)

    train_images_centered, mean_image = preprocess_data(train_images)
    test_images_centered = test_images - mean_image

    two_dpca = TwoDPCA(threshold=0.95)
    two_dpca.fit(train_images_centered)
    train_projected = two_dpca.transform(train_images_centered)
    test_projected = two_dpca.transform(test_images_centered)

    print(f'Projected training data shape: {train_projected.shape}')
    print(f'Projected test data shape: {test_projected.shape}')
