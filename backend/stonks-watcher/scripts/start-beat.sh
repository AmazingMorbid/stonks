#!/bin/bash

celery -A celeryapp beat -l info

