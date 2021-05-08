#!/bin/bash

celery -A celeryapp worker -l info
