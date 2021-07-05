# Retarded-webcamera-server
*Literally a retarded localhost webcamera server*

First of all we wanted to stream webcamera feed to localhost. Accepting that *motion* linux package was not an option we decided to find our own way to achieve our goal.

We've spent 4 hours trying to implement it using cv2 with acceptable FPS (just in case: it was running on 6y old lenovo) to find out that somebody have already done it using v4l2...

After 2 more hours of pain we gave up, tweaked some settings and executed ```git push --force --no-verify```


## Installation 
```python3 -m venv venv```

```source venv/bin/activate```

```pip install -r requirements.txt```

## Prerequirements
```export CAMERA_ID=<your_camera_id from /dev/video*>```

## Production run (ofc it will be run in prod)
```gunicorn --bind 0.0.0.0:5000 wsgi:app -t 0 --threads=64```

## Debug run (preferred)
```python app.py```
