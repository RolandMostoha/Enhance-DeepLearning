# Enhance - DeepLearning

Enhance is Tensorflow based regression project. Its primary goal is to make predictions based on your personal fitness goals using your Fitbit (or a custom provider's) health records.

It's purpose is my personal entertainment, I consider it as a hobby project where I can try what I've learnt in my journey of deep learning.

## Main concept

To demonstrate the main idea behind the project, let's suppose we have a dataset with the following features:

record_date | weight | fat | cal_out | rest_heart | active_min | inactive_min | sleep | ... |
--- | --- | --- | --- | --- | --- | --- | --- |  --- |
2020-10-10 | 77kg | 22% | 2500 | 65 | 120m | 600m | 8hr | ... |
2020-10-11 | 76kg | 22% | 3000 | 64 | 0m | 650m | 8hr | ... |
... | ... | ... | ... | ... | ... | ... | ... | ... |

Let's say we want to make a goal by reducing the **fat percentage to 18%**.

The network can make predictions about what other features to change to achieve the goal. Something similar like:

```
Predicted weight value for my goal: [[72.58874]]
Predicted total_calories value for my goal: [[2451.2554]]
Predicted resting_heart value for my goal: [[60.58874]]
Predicted sedentary_minutes value for my goal: [[730.1085]]
Predicted highly_active_minutes value for my goal: [[68.19724]]
Predicted sleep_duration value for my goal: [[510.2371]]
...
```

## How does it work

Let's suppose we have *N* type of health records, and we want to change *m* features by defining a goal. 

The network creates *N-m* models and uses the latest health record merged with the goal as an input and make *N-m* predictions by the trained models.

## Usage

A good outline of the project can be the following Jupyter notebook: [notebooks/enhance.ipynb](notebooks/enhance.ipynb) 

There is also a corresponding `main/main.py` which can be run as a Python script.

The recommended steps to run the project:

1. Register a Fitbit Developer account
2. Authenticate via Fitbit
3. Load Fitbit health records via Fitbit Developer API
4. Process the generated dataset with Pandas
5. Define your goal
6. Train the model
7. Evaluate predictions

### Fitbit integration

You'll need a Fitbit developer account to load your health records using the Fitbit Developer API. 

1. Sign up here: https://www.fitbit.com/signup
2. Register an application in https://dev.fitbit.com/ under *Manage*
   * OAuth 2.0 Application Type *: `Personal`
   * Callback URL *: `http://127.0.0.1:8080/`
3. Set the generated Client ID and Client Secret in `configs/fitbit_auth_config.json`

After the successful authentication, you can use the `FitbitDataProvider` to collect your health records. 

If you want to add more features, you can update the `src/model/records.py` and extend the `FitbitDataProvider` class. 

### Custom data provider

You can also use a custom data provider by implementing the `DataProvider` class, which is an `abc.ABC` class. 

### Random data provider

If you just want to try out the project without any custom data provider, you can use `RandomDataProvider`.

### Custom trainer

You can customize the trainers or write a new one besides the built-in ones:

`src/trainer/LinearRegressionTrainer`

`src/trainer/DNNTrainer`

## Project structure

```
├──  configs  
│    └── fitbit_auth_config.json - storing client id and client secret
│
├──  data - storing the generated raw datasets  
│
├──  main
│   ├── main.py
│
├── notebooks
│   └── enhance.ipynb
│
├── src             - source folder for python files
│   └── auth        - Authentication scripts for Fitbit
|   └── data        - data loading and dataset generation
│       └── model       - model representations of health records
│       └── provider    - data providers
|   └── plotter
|   └── trainer     - Tensorflow trainer implementations  
|   └── utils
│
├── tests           - pytest unit tests for data generation
```