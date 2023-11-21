import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from skorch import NeuralNetRegressor
from skorch.callbacks import EarlyStopping

# Load data from CSV files
x_data_file = "MODEL_DATA/NEWDATA/newData_combined_FD.csv"
y_data_file = "MODEL_DATA/NEWDATA/newData_expanded_realHardParam.csv"

x_data = pd.read_csv(x_data_file)
y_data = pd.read_csv(y_data_file)

# Split the data into X (input features) and Y (target - c-parameters)
X_data = x_data.values.astype(np.float32)
Y_data = y_data.values.astype(np.float32)

# Create Min-Max scalers for input data and target values
input_scaler = MinMaxScaler()
X_data_scaled = input_scaler.fit_transform(X_data)

target_scaler = MinMaxScaler()
Y_data_scaled = target_scaler.fit_transform(Y_data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_data_scaled, Y_data_scaled, test_size=0.2, random_state=42)

# Define a custom neural network model
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, hidden_size3, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.LeakyReLU(negative_slope=0.01)
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.LeakyReLU(negative_slope=0.01)
        self.fc3 = nn.Linear(hidden_size2, hidden_size3)  # New hidden layer
        self.relu3 = nn.LeakyReLU(negative_slope=0.01)     # New activation function
        self.fc4 = nn.Linear(hidden_size3, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.relu3(x)
        x = self.fc4(x)
        return x

# Create a Skorch wrapper for the neural network with Early Stopping
net = NeuralNetRegressor(
    module=NeuralNetwork,
    module__input_size=X_data.shape[1],
    module__hidden_size1=256,
    module__hidden_size2=256,
    module__hidden_size3=128,   # New hidden layer size
    module__output_size=Y_data.shape[1],
    criterion=nn.MSELoss,
    optimizer=optim.Adam,
    optimizer__lr=0.0005,
    max_epochs=3000,
    callbacks=[EarlyStopping(patience=20)],
    device='cuda' if torch.cuda.is_available() else 'cpu',  # Use GPU if available
)

# Train the model
history = net.fit(X_train, y_train)

# Extract the training and validation losses from the history
train_losses = history.history[:, 'train_loss']
valid_losses = history.history[:, 'valid_loss']

# Evaluate the model on the test set
y_pred = net.predict(X_test)

# Inverse scale the predictions to the original range
y_pred_original = target_scaler.inverse_transform(y_pred)
y_test_original = target_scaler.inverse_transform(y_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test_original, y_pred_original)
mse = mean_squared_error(y_test_original, y_pred_original)
r2 = r2_score(y_test_original, y_pred_original)

print(f'Mean Absolute Error: {mae:.4f}')
print(f'Mean Squared Error: {mse:.4f}')
print(f'R-squared (R2) Score: {r2:.4f}')

# Save the trained model
torch.save(net.module_.state_dict(), 'trained_model.pth')

# Load the trained model for prediction
net.module_.load_state_dict(torch.load('trained_model.pth'))
net.module_.eval()

# Example prediction for a single input (you can replace this with your data)
X_example = X_test[0]
X_example_tensor = torch.tensor(X_example, dtype=torch.float32)
with torch.no_grad():
    prediction = net.module_(X_example_tensor.unsqueeze(0))  # Unsqueeze to add batch dimension

# Inverse scale the prediction to the original range
prediction_original = target_scaler.inverse_transform(prediction.numpy())

# Print the predicted 'c-parameters'
predicted_parameters = prediction_original[0].tolist()
print(f'Predicted c-parameters:')
print(prediction_original[0].tolist())

# val error usually around 0.07
# r-squared value usually around 0.5 