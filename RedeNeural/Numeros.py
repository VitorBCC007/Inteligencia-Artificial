import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# Carregar o conjunto de dados MNIST
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Pré-processamento dos dados
train_images = train_images / 255.0
test_images = test_images / 255.0

# Definir a arquitetura da rede neural
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compilar o modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Treinar a rede neural
model.fit(train_images, train_labels, epochs=3)

# Avaliar a acurácia do modelo
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Acurácia do teste:", test_acc)

# Adicionar ruído às imagens de teste
noise_factor = 0.0
test_images_noisy = test_images + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=test_images.shape)
test_images_noisy = np.clip(test_images_noisy, 0.0, 1.0)

# Fazer previsões com o modelo treinado usando as imagens ruidosas
predictions = model.predict(test_images_noisy)

# Exibir algumas imagens de teste com ruído e suas previsões
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(test_images_noisy[i], cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions[i])
    true_label = test_labels[i]
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    plt.xlabel("{} ({})".format(predicted_label, true_label), color=color)
plt.show()
