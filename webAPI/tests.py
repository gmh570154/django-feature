from django.test import TestCase

# Create your tests here.
import os

from .models import PageView
from .database import info
from django.test import TestCase

# These basic tests are to be used as an example for running tests in S2I
# and OpenShift when building an application image.

