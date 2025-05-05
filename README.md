# Deploy Flask App on Google Cloud VM
## Step 1: Authenticate with Google Cloud and SSH into Your VM
1. Login:

    ```
    gcloud auth login
    ```

2. Set Your Active Project:

    ```
    gcloud config set project PROJECT-ID
    ```

3. To confirm it's set:

    ```
    gcloud config list project
    ```
4. SSH into instance:
    
    ```
    gcloud compute ssh INSTANCE_NAME --project PROJECT_ID --zone ZONE
    ```

## Step 2: Install Required Software:
Make sure Python, pip, Git, and virtualenv are installed:

```
    sudo apt update
    sudo apt install python3-pip python3-venv git -y
```
## Step 3: Clone Repository:

```
    cd ~
    git clone https://github.com/maggie197/Posty.git
    cd Posty

```

## Step 4: Install flask_login and any other dependencies manually

```
    pip install flask flask_login flask_sqlalchemy
```
## Step 5: Create Virtual Environment and Install Dependencies
```
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```

## Step 6: Test the App
 Run the app to make sure it works locally:

```
    python app.py

```

## Step 7: Manually Create a Firewall Rule 

1. Go to: GCP → VPC network → Firewall rules

2. Click Create firewall rule

3. Fill in:

    1. Name: allow-http

    2. Targets: All instances in the network

    3. Source IP ranges: 0.0.0.0/0

    4. Protocols and ports: Select “Specified protocols and ports” → check tcp and type 80

4. Click Create

## Step 8: Run Flask App on Public IP

```
    sudo venv/bin/python app.py

```
## Step 9: Visit Your Flask App

Go to:
    http://[YOUR_EXTERNAL_VM_IP]