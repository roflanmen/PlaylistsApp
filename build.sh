cd client
npm run build
cd ..
gunicorn --worker-class eventlet -w 1 run:app