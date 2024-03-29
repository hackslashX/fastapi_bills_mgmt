"""
Base Routing. Includes all routing information and mapping of URLs
"""
from abc import abstractmethod
from fastapi_restful import Api

from instance.config import config


class BaseRouting(object):
    api: Api
    api_version: str
    app = None
    base_url = config.API_PREFIX

    def __init__(self, app):
        self.app = app
        self.api = Api(app)
        self.routing_collection = {}

    @abstractmethod
    def set_routing_collection(self):
        raise NotImplementedError

    def add_resources(self):
        """
        Add resources to the API
        """

        for _, api_details in self.routing_collection.items():
            resource, url = api_details
            url = f"/{self.base_url}/{self.api_version}/{url}"
            self.api.add_resource(resource, url)

    def map_urls(self):
        """
        Map the URLs to the resources
        """

        self.set_routing_collection()
        self.add_resources()
