To build the docker image, run
```
docker build -t flare-i2b2-fhirsearch .
```

When the build was successful, you can run the image via
```
docker run -d -p 5000:5000 flare-i2b2-fhirsearch
```
