# Get Started

To run the exampled from this repo, it is enough to make the start_demo script working.


Clone this repostory and the pygeapi Iliad fork

```
clone https://github.com/pzaborowski/pygeoapi.git
clone https://github.com/ILIAD-ocean-twin/data_access_api.git
```

Set the environment variable paths in the data_access_api/examples/start_demo or environment and uncomment:

```
#export Iliad_api_repo=[path to the data_access_api repository]
#export Iliad_pygeoapi_repo=[path to the pygeoapi repository]
```

for Unix environment, change 
```
sed -i '' 's|\[data\ path\]|/Users/piotr/repos/Iliad/data_access_api/examples/data|g' example-config.yml
```
to
```
sed -i 's|\[data\ path\]|/Users/piotr/repos/Iliad/data_access_api/examples/data|g' example-config.yml
```

run the data_access_api/examples/start_demo
```
chmod +x data_access_api/examples/start_demo
cd data_access_api/examples/
./start_demo
```

Open http://localhost:5002/collections
it shall open following screen
![image](../images/collections-example.png)

