# Install psql client
apt update -y
apt-get install postgresql-client -y

# Run app
python3 -m streamlit run Dashboard.py