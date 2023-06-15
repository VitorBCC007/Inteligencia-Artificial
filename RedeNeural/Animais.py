import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# Carregar o conjunto de dados CIFAR-10
cifar10 = keras.datasets.cifar10
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Pré-processamento dos dados
train_images = train_images / 255.0
test_images = test_images / 255.0

# Função para adicionar ruído gaussiano a uma imagem
def add_gaussian_noise(image, std_dev):
    noise = np.random.normal(loc=0, scale=std_dev, size=image.shape)
    noisy_image = image + noise
    noisy_image = np.clip(noisy_image, 0.0, 1.0)  # Garantir que os valores dos pixels estejam entre 0 e 1
    return noisy_image

# Adicionar ruído gaussiano às imagens de treinamento
std_dev = 0.0  # Desvio padrão do ruído gaussiano
noisy_train_images = np.array([add_gaussian_noise(image, std_dev) for image in train_images])

# Adicionar ruído gaussiano às imagens de teste
noisy_test_images = np.array([add_gaussian_noise(image, std_dev) for image in test_images])

# Definir a arquitetura da rede neural
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compilar o modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Treinar a rede neural com as imagens ruidosas
model.fit(noisy_train_images, train_labels, epochs=1)

# Avaliar a acurácia do modelo usando as imagens de teste ruidosas
test_loss, test_acc = model.evaluate(noisy_test_images, test_labels)
print("Acurácia do teste:", test_acc)

# Fazer previsões com o modelo treinado
predictions = model.predict(noisy_test_images)

# Exibir algumas imagens de teste ruidosas e suas previsões
class_names = ['Avião', 'Automóvel', 'Pássaro', 'Gato', 'Veado', 'Cachorro', 'Sapo', 'Cavalo', 'Navio', 'Caminhão']

plt.figure(figsize=(10, 10))
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(noisy_test_images[i], cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions[i])
    true_label = test_labels[i][0]
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    plt.xlabel("{} ({})".format(class_names[predicted_label], class_names[true_label]), color=color)
plt.show()
