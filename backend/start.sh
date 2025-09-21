#!/bin/bash
gunicorn api:app --bind=0.0.0.0:$PORT