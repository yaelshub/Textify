import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split


def train_author_classifier(csv_paths: dict, model_output_path: str = 'author_identifier_model.pkl'):
    dataframes = []
    # Read and combine the data
    for author, path in csv_paths.items():
        try:
            df = pd.read_csv(path)
            df['author'] = author
            dataframes.append(df)
            print(f"Loaded data for {author}: {len(df)} samples")
        except FileNotFoundError:
            print(f"Warning: File not found for {author}: {path}")
            continue
        except Exception as e:
            print(f"Error loading data for {author}: {e}")
            continue
    
    if not dataframes:
        raise ValueError("No valid data files were loaded")
    
    # Combine all dataframes
    data = pd.concat(dataframes, ignore_index=True)
    print(f"Total combined data: {len(data)} samples")
    
    # Check if we have the required columns
    if 'author' not in data.columns:
        raise ValueError("'author' column not found in the data")
    
    # Separate features (X) and labels (y)
    X = data.drop('author', axis=1)
    y = data['author']
    
    # Check for non-numeric features and handle them
    non_numeric_cols = X.select_dtypes(exclude=['number']).columns
    if len(non_numeric_cols) > 0:
        print(f"Warning: Non-numeric columns found: {list(non_numeric_cols)}")
        print("These columns will be dropped. Consider encoding them if they're important features.")
        X = X.select_dtypes(include=['number'])
    
    if X.empty:
        raise ValueError("No numeric features found for training")
    
    print(f"Features shape: {X.shape}")
    print(f"Unique authors: {y.nunique()}")
    
    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Initialize and train the model
    model = xgb.XGBClassifier(
        random_state=42,
        eval_metric='mlogloss'  # Suppress warning for multiclass
    )
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    # Test model performance
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save the model
    try:
        joblib.dump(model, model_output_path)
        print(f"Model saved as {model_output_path}")
    except Exception as e:
        print(f"Error saving model: {e}")
    
    return model, accuracy


# Example usage:
if __name__ == "__main__":
    csv_paths = {
        'author1': 'D:\Textify\server\data\Charles_Dickens.csv',
        'author2': 'D:\Textify\server\data\H. G. Wells.csv',
        'author3': 'D:\Textify\server\data\Jane_Austen.csv',
        'author4': 'D:\Textify\server\data\Mark_Twain.csv'
    }
    try:
        model, accuracy = train_author_classifier(csv_paths)
        print(f"Training completed successfully with {accuracy:.2%} accuracy")
    except Exception as e:
        print(f"Training failed: {e}")