BASE='/home/twilight/py/mywebsite/admin'
pushd $BASE
pushd admin-frontend
npm start > /dev/null &
popd
pushd staging
jupyter lab & 
popd
pushd admin-backend
source venv/bin/activate
python3 app.py &
wait
echo "All done\n"
