import asyncio
from bleak import BleakClient

from pycycling.cycling_power_service import CyclingPowerService

async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            #print(data)
            instant_power = data.instantaneous_power
            print("You cycle " + str(instant_power) + " Watt")
        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(60.0)
        await trainer.disable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "E7:3D:B8:0D:7A:FB"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))