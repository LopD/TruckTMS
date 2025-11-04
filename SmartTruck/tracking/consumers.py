## 3rd party
import asyncio
import httpx
import json
from urllib.parse import parse_qs

## channels 
## https://channels.readthedocs.io/en/latest/
from channels.generic.websocket import AsyncWebsocketConsumer

## rest_framework
from rest_framework_simplejwt.tokens import UntypedToken,AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .permissions import VehicleTrackingPermission



class VehicleTrackingConsumer(AsyncWebsocketConsumer):

    def get_user_groups(validated_token) -> list:
        """
        Helper function for getting the user groups from a validated token.
        """
        groups = validated_token.get("groups",[])
        return groups

    # ALLOW_ANON_USERS = False                            ## are anonymous users allowed access
    # ALLOWED_USER_GROUPS = ['Dispatchers']               ## Which user groups are allowed access
    permission_classes = [VehicleTrackingPermission]    ## custom permission class that is not inheriting rest_framework.permissions.BasePermission

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_permission(self) -> bool:
        """
        Checks if 'self.scope' is properly set up and passes all the permission classes
        """
        for perm_class in self.permission_classes:
            if not perm_class().has_permission(scope=self.scope):
                return False
        return True

    async def connect(self):
        
        self.polling_task = None                        ## function pointer to the polling function
        self.current_vehicle_id = None                  ## vehicle id that's being polled

        if not self.has_permission():
            await self.close(code=4003)
            return

        # ## check if anonymous users are allowed access
        # if not self.ALLOW_ANON_USERS:
        #     user = self.scope["user"]
        #     # print('VehicleTrackingConsumer=>user=',user)
        #     if not user or not user.is_authenticated:
        #         await self.close(code=4003)
        #         return

        # ## check if the user is in any group in ALLOWED_USER_GROUPS
        # ## check via the access token
        # if not self.ALLOW_ANON_USERS and len(self.ALLOWED_USER_GROUPS) > 0:    
        #     user_groups = self.scope["groups"]
        #     if not any(user_group in self.ALLOWED_USER_GROUPS for user_group in user_groups):
        #         await self.close(code=4003)
        #         return

        await self.accept()
        # await self.channel_layer.group_add("truck_tracking", self.channel_name)


    async def disconnect(self, close_code):
        
        ## stop the polling loop
        if self.polling_task:
            self.polling_task.cancel()
        # await self.channel_layer.group_discard("truck_tracking", self.channel_name)


    async def receive(self, text_data):
        '''
        Starts the polling loop if it is not polling.
        Changes the vehicle_id of the polling loop if it is already working.
        '''
        data = json.loads(text_data)
        vehicle_id = data.get("vehicle_id")

        if not vehicle_id:
            await self.send(text_data=json.dumps({"error": "vehicle_id is required"}))
            return

        # Cancel previous task if exists
        if self.polling_task:
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                pass

        self.current_vehicle_id = vehicle_id
        self.polling_task = asyncio.create_task(self.poll_vehicle_loop(vehicle_id))


    async def poll_vehicle_loop(self, vehicle_id, sleep_duration=5):
        '''
        Infinite loop that sends get requests to gomotive api.
        '''
        try:
            while True:
                try:
                    location = await self.get_vehicle_location(vehicle_id)
                    await self.send(text_data=json.dumps({
                        "vehicle_id": vehicle_id,
                        "location": location,
                    }))
                except Exception as e:
                    await self.send(text_data=json.dumps({
                        "error": str(e),
                        "vehicle_id": vehicle_id,
                    }))
                await asyncio.sleep(sleep_duration)
        except asyncio.CancelledError:
            pass


    async def get_vehicle_location(self, vehicle_id):
        url = f"https://api.gomotive.com/v1/vehicle_locations?vehicle_ids={vehicle_id}"
        headers = {
            "x-api-key": "30d634dc-d64b-478d-b576-9a4229d587c2",
            "accept": "application/json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            vehicle_location = data.get('vehicles',None)
            if vehicle_location is None or len(vehicle_location) < 0:
                raise Exception("Vehicle not found!")
            vehicle_location = vehicle_location[0].get('vehicle').get('current_location')
            return vehicle_location  # or data['vehicles'][0] if API returns a list


    # async def send(self, text_data=None, bytes_data=None):
    #     print('TrackingConsumer send')
    #     pass

    # async def send_location(self, event):
    #     print('TrackingConsumer sending location...')
    #     await self.send(text_data=json.dumps(event["location"]))
