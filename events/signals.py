"""Signals for the events app."""
from django import dispatch

post_guest_create = dispatch.Signal(providing_args=['user', 'event'])
