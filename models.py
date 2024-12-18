from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
import matplotlib.pyplot as plt
import polars as pl
import numpy as np
import pandas as pd
import math
import pickle
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input


class LaptopPredictionModel:
    def __init__(self, model: str, columns: list, params: dict | None = None):
        self.columns = columns
        if model == "xgb":
            self.model = XGBRegressor()
            self.grid_search = True
            self.scaler = False
        elif model == "rdf":
            self.model = RandomForestRegressor()
            self.grid_search = True
            self.scaler = False
        elif model == "lnr":
            self.model = LinearRegression()
            self.grid_search = False
            self.scaler = True
        elif model == "ann":
            self.model = self._build_ann()
            self.grid_search = False
            self.scaler = True
        else:
            raise ValueError("Unsupported model type. Choose from 'xgb', 'rdf', 'lnr', or 'ann'.")

        self.params = params

    def _build_ann(self):
        """Define the architecture of the ANN."""
        model = Sequential()
        model.add(Input(shape=(len(self.columns),)))  # Use the number of columns for input shape
        model.add(Dense(128, activation='relu'))  # Hidden layer
        model.add(Dense(64, activation='relu'))  # Another hidden layer
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1))  # Output layer for regression
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        return model

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        print(f"Training {self.model.__class__.__name__ if not hasattr(self.model, 'name') else 'ANN'}")

        if self.scaler:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            self.scaler = scaler

        if isinstance(self.model, Sequential):
            early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            history = self.model.fit(
                X_train, y_train,
                validation_split=0.2,  # Use 20% of the data for validation
                epochs=200,
                batch_size=32,
                callbacks=[early_stop],
                verbose=1
            )
            y_pred_train = self.model.predict(X_train).squeeze()
            self._plot_ann_training(history)
        elif self.grid_search:
            self.grid = GridSearchCV(
                estimator=self.model, param_grid=self.params, cv=5,
                verbose=1, n_jobs=-1, refit=True,
            )
            self.grid.fit(X_train, y_train)
            y_pred_train = self.grid.predict(X_train)
            self._save_model()
        else:
            self.model.fit(X_train, y_train)
            y_pred_train = self.model.predict(X_train)

        return self._evaluate(y_train, y_pred_train)

    def predict(self, X_test: np.ndarray):
        """Make predictions on test data."""
        if self.scaler:
            X_test = self.scaler.transform(X_test)

        if isinstance(self.model, Sequential):
            return self.model.predict(X_test).squeeze()
        else:
            return self.model.predict(X_test)

    def _evaluate(self, y_test, y_pred):
        metrics = {
            "Model": "ANN" if isinstance(self.model, Sequential) else self.model.__class__.__name__,
            'MAPE Test (%)': round(math.sqrt(mean_absolute_percentage_error(y_test, y_pred)), 4) * 100,
            'MAE Test': round(mean_absolute_error(y_test, y_pred), 4),
            'R2 Score Test': round(r2_score(y_test, y_pred), 4),
        }

        # Convert metrics to a polars DataFrame
        metrics_df = pl.DataFrame([metrics])
        print(metrics_df)
        return metrics_df  # Ensure metrics are returned as a DataFrame

    def _plot_ann_training(self, history):
        plt.figure(figsize=(12, 6))
        plt.plot(history.history['loss'], label='Training Loss')
        plt.title("Training Loss")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

    def _plot_regression(self, y_test, y_pred):
        plt.subplot(1, 2, 2)
        plt.scatter(y_test, y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title("Comparison")

    def _save_model(self):
        os.makedirs("./checkpoint", exist_ok=True)
        with open(f"./checkpoint/{self.model.__class__.__name__}.pkl", "wb") as f:
            pickle.dump(self.grid.best_estimator_, f)

