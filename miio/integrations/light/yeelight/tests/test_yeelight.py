from unittest import TestCase

import pytest

from miio.tests.dummies import DummyDevice

from .. import Yeelight, YeelightException, YeelightMode, YeelightStatus
from ..spec_helper import YeelightSpecHelper, YeelightSubLightType


class DummyLight(DummyDevice, Yeelight):
    def __init__(self, *args, **kwargs):
        self._model = "missing.model.yeelight"

        self.return_values = {
            "get_prop": self._get_state,
            "set_power": lambda x: self._set_state("power", x),
            "set_bright": lambda x: self._set_state("bright", x),
            "set_ct_abx": lambda x: self._set_state("ct", x),
            "set_rgb": lambda x: self._set_state("rgb", x),
            "set_hsv": lambda x: self._set_state("hsv", x),
            "set_name": lambda x: self._set_state("name", x),
            "set_ps": lambda x: self.set_config(x),
            "toggle": self.toggle_power,
            "set_default": lambda x: "ok",
        }

        super().__init__(*args, **kwargs)
        if Yeelight._spec_helper is None:
            Yeelight._spec_helper = YeelightSpecHelper()
            Yeelight._supported_models = Yeelight._spec_helper.supported_models

        self._model_info = Yeelight._spec_helper.get_model_info(self.model)
        self._light_type = YeelightSubLightType.Main
        self._light_info = self._model_info.lamps[self._light_type]
        self._color_temp_range = self._light_info.color_temp

    def set_config(self, x):
        key, value = x
        config_mapping = {"cfg_lan_ctrl": "lan_ctrl", "cfg_save_state": "save_state"}

        self._set_state(config_mapping[key], [value])

    def toggle_power(self, _):
        if self.state["power"] == "on":
            self.state["power"] = "off"
        else:
            self.state["power"] = "on"


class DummyCommonBulb(DummyLight):
    def __init__(self, *args, **kwargs):
        self.state = {
            "name": "test name",
            "lan_ctrl": "1",
            "save_state": "1",
            "delayoff": "0",
            "music_on": "1",
            "power": "off",
            "bright": "100",
            "color_mode": "2",
            "rgb": "",
            "hue": "",
            "sat": "",
            "ct": "3584",
            "flowing": "",
            "flow_params": "",
            "active_mode": "",
            "nl_br": "",
            "bg_power": "",
            "bg_bright": "",
            "bg_lmode": "",
            "bg_rgb": "",
            "bg_hue": "",
            "bg_sat": "",
            "bg_ct": "",
            "bg_flowing": "",
            "bg_flow_params": "",
        }
        super().__init__(*args, **kwargs)


@pytest.fixture(scope="class")
def dummycommonbulb(request):
    request.cls.device = DummyCommonBulb()
    # TODO add ability to test on a real device


@pytest.mark.usefixtures("dummycommonbulb")
class TestYeelightCommon(TestCase):
    def test_on(self):
        self.device.off()  # make sure we are off
        assert self.device.status().is_on is False

        self.device.on()
        assert self.device.status().is_on is True

    def test_off(self):
        self.device.on()  # make sure we are on
        assert self.device.status().is_on is True

        self.device.off()
        assert self.device.status().is_on is False

    def test_set_brightness(self):
        def brightness():
            return self.device.status().brightness

        self.device.set_brightness(50)
        assert brightness() == 50
        self.device.set_brightness(0)
        assert brightness() == 0
        self.device.set_brightness(100)

        with pytest.raises(YeelightException):
            self.device.set_brightness(-100)

        with pytest.raises(YeelightException):
            self.device.set_brightness(200)

    def test_set_color_temp(self):
        def color_temp():
            return self.device.status().color_temp

        self.device.set_color_temp(2000)
        assert color_temp() == 2000
        self.device.set_color_temp(6500)
        assert color_temp() == 6500

        with pytest.raises(YeelightException):
            self.device.set_color_temp(1000)

        with pytest.raises(YeelightException):
            self.device.set_color_temp(7000)

    def test_set_developer_mode(self):
        def dev_mode():
            return self.device.status().developer_mode

        orig_mode = dev_mode()
        self.device.set_developer_mode(not orig_mode)
        new_mode = dev_mode()
        assert new_mode is not orig_mode
        self.device.set_developer_mode(not new_mode)
        assert new_mode is not dev_mode()

    def test_set_save_state_on_change(self):
        def save_state():
            return self.device.status().save_state_on_change

        orig_state = save_state()
        self.device.set_save_state_on_change(not orig_state)
        new_state = save_state()
        assert new_state is not orig_state
        self.device.set_save_state_on_change(not new_state)
        new_state = save_state()
        assert new_state is orig_state

    def test_set_name(self):
        def name():
            return self.device.status().name

        assert name() == "test name"
        self.device.set_name("new test name")
        assert name() == "new test name"

    def test_toggle(self):
        def is_on():
            return self.device.status().is_on

        orig_state = is_on()
        self.device.toggle()
        new_state = is_on()
        assert orig_state != new_state

        self.device.toggle()
        new_state = is_on()
        assert new_state == orig_state

    @pytest.mark.skip("cannot be tested easily")
    def test_set_default(self):
        self.fail()

    @pytest.mark.skip("set_scene is not implemented")
    def test_set_scene(self):
        self.fail()


class DummyLightСolor(DummyLight):
    def __init__(self, *args, **kwargs):
        self.state = {
            "name": "test name",
            "lan_ctrl": "1",
            "save_state": "1",
            "delayoff": "0",
            "music_on": "1",
            "power": "off",
            "bright": "100",
            "color_mode": "2",
            "rgb": "16711680",
            "hue": "359",
            "sat": "100",
            "ct": "3584",
            "flowing": "0",
            "flow_params": "0,0,1000,1,16711680,100,1000,1,65280,100,1000,1,255,100",
            "active_mode": "",
            "nl_br": "",
            "bg_power": "",
            "bg_bright": "",
            "bg_lmode": "",
            "bg_rgb": "",
            "bg_hue": "",
            "bg_sat": "",
            "bg_ct": "",
            "bg_flowing": "",
            "bg_flow_params": "",
        }
        super().__init__(*args, **kwargs)


@pytest.fixture(scope="class")
def dummylightcolor(request):
    request.cls.device = DummyLightСolor()
    # TODO add ability to test on a real device


@pytest.mark.usefixtures("dummylightcolor")
class TestYeelightLightColor(TestCase):
    def test_status(self):
        self.device._reset_state()
        status = self.device.status()  # type: YeelightStatus

        assert repr(status) == repr(YeelightStatus(self.device.start_state))

        assert status.name == self.device.start_state["name"]
        assert status.developer_mode is True
        assert status.save_state_on_change is True
        assert status.delay_off == 0
        assert status.music_mode is True
        assert len(status.lights) == 1
        assert status.is_on is False and status.is_on == status.lights[0].is_on
        assert (
            status.brightness == 100
            and status.brightness == status.lights[0].brightness
        )
        assert (
            status.color_mode == YeelightMode.ColorTemperature
            and status.color_mode == status.lights[0].color_mode
        )
        assert (
            status.color_temp == 3584
            and status.color_temp == status.lights[0].color_temp
        )
        assert status.rgb is None and status.rgb == status.lights[0].rgb
        assert status.hsv is None and status.hsv == status.lights[0].hsv
        # following are tested in set mode tests
        # assert status.rgb == 16711680
        # assert status.hsv == (359, 100, 100)
        assert (
            status.color_flowing is False
            and status.color_flowing == status.lights[0].color_flowing
        )
        assert (
            status.color_flow_params is None
            and status.color_flow_params == status.lights[0].color_flow_params
        )
        # color_flow_params will be tested after future implementation
        # assert status.color_flow_params == "0,0,1000,1,16711680,100,1000,1,65280,100,1000,1,255,100" and status.color_flow_params == status.lights[0].color_flow_params
        assert status.moonlight_mode is None
        assert status.moonlight_mode_brightness is None

    def test_set_rgb(self):
        def rgb():
            return self.device.status().rgb

        self.device._reset_state()
        self.device._set_state("color_mode", [1])

        assert rgb() == (255, 0, 0)

        self.device.set_rgb((0, 0, 1))
        assert rgb() == (0, 0, 1)
        self.device.set_rgb((255, 255, 0))
        assert rgb() == (255, 255, 0)
        self.device.set_rgb((255, 255, 255))
        assert rgb() == (255, 255, 255)

        with pytest.raises(YeelightException):
            self.device.set_rgb((-1, 0, 0))

        with pytest.raises(YeelightException):
            self.device.set_rgb((256, 0, 0))

        with pytest.raises(YeelightException):
            self.device.set_rgb((0, -1, 0))

        with pytest.raises(YeelightException):
            self.device.set_rgb((0, 256, 0))

        with pytest.raises(YeelightException):
            self.device.set_rgb((0, 0, -1))

        with pytest.raises(YeelightException):
            self.device.set_rgb((0, 0, 256))

    @pytest.mark.skip("hsv is not properly implemented")
    def test_set_hsv(self):
        self.reset_state()
        hue, sat, val = self.device.status().hsv
        assert hue == 359
        assert sat == 100
        assert val == 100

        self.device.set_hsv()


class DummyLightCeilingV1(DummyLight):  # without background light
    def __init__(self, *args, **kwargs):
        self.state = {
            "name": "test name",
            "lan_ctrl": "1",
            "save_state": "1",
            "delayoff": "0",
            "music_on": "",
            "power": "off",
            "bright": "100",
            "color_mode": "2",
            "rgb": "",
            "hue": "",
            "sat": "",
            "ct": "3584",
            "flowing": "0",
            "flow_params": "0,0,2000,3,0,33,2000,3,0,100",
            "active_mode": "1",
            "nl_br": "100",
            "bg_power": "",
            "bg_bright": "",
            "bg_lmode": "",
            "bg_rgb": "",
            "bg_hue": "",
            "bg_sat": "",
            "bg_ct": "",
            "bg_flowing": "",
            "bg_flow_params": "",
        }
        super().__init__(*args, **kwargs)


@pytest.fixture(scope="class")
def dummylightceilingv1(request):
    request.cls.device = DummyLightCeilingV1()
    # TODO add ability to test on a real device


@pytest.mark.usefixtures("dummylightceilingv1")
class TestYeelightLightCeilingV1(TestCase):
    def test_status(self):
        self.device._reset_state()
        status = self.device.status()  # type: YeelightStatus

        assert repr(status) == repr(YeelightStatus(self.device.start_state))

        assert status.name == self.device.start_state["name"]
        assert status.developer_mode is True
        assert status.save_state_on_change is True
        assert status.delay_off == 0
        assert status.music_mode is None
        assert len(status.lights) == 1
        assert status.is_on is False and status.is_on == status.lights[0].is_on
        assert (
            status.brightness == 100
            and status.brightness == status.lights[0].brightness
        )
        assert (
            status.color_mode == YeelightMode.ColorTemperature
            and status.color_mode == status.lights[0].color_mode
        )
        assert (
            status.color_temp == 3584
            and status.color_temp == status.lights[0].color_temp
        )
        assert status.rgb is None and status.rgb == status.lights[0].rgb
        assert status.hsv is None and status.hsv == status.lights[0].hsv
        # following are tested in set mode tests
        # assert status.rgb == 16711680
        # assert status.hsv == (359, 100, 100)
        assert (
            status.color_flowing is False
            and status.color_flowing == status.lights[0].color_flowing
        )
        assert (
            status.color_flow_params is None
            and status.color_flow_params == status.lights[0].color_flow_params
        )
        # color_flow_params will be tested after future implementation
        # assert status.color_flow_params == "0,0,1000,1,16711680,100,1000,1,65280,100,1000,1,255,100" and status.color_flow_params == status.lights[0].color_flow_params
        assert status.moonlight_mode is True
        assert status.moonlight_mode_brightness == 100


class DummyLightCeilingV2(DummyLight):  # without background light
    def __init__(self, *args, **kwargs):
        self.state = {
            "name": "test name",
            "lan_ctrl": "1",
            "save_state": "1",
            "delayoff": "0",
            "music_on": "",
            "power": "off",
            "bright": "100",
            "color_mode": "2",
            "rgb": "",
            "hue": "",
            "sat": "",
            "ct": "3584",
            "flowing": "0",
            "flow_params": "0,0,2000,3,0,33,2000,3,0,100",
            "active_mode": "1",
            "nl_br": "100",
            "bg_power": "off",
            "bg_bright": "100",
            "bg_lmode": "2",
            "bg_rgb": "15531811",
            "bg_hue": "65",
            "bg_sat": "86",
            "bg_ct": "4000",
            "bg_flowing": "0",
            "bg_flow_params": "0,0,3000,4,16711680,100,3000,4,65280,100,3000,4,255,100",
        }
        super().__init__(*args, **kwargs)


@pytest.fixture(scope="class")
def dummylightceilingv2(request):
    request.cls.device = DummyLightCeilingV2()
    # TODO add ability to test on a real device


@pytest.mark.usefixtures("dummylightceilingv2")
class TestYeelightLightCeilingV2(TestCase):
    def test_status(self):
        self.device._reset_state()
        status = self.device.status()  # type: YeelightStatus

        assert repr(status) == repr(YeelightStatus(self.device.start_state))

        assert status.name == self.device.start_state["name"]
        assert status.developer_mode is True
        assert status.save_state_on_change is True
        assert status.delay_off == 0
        assert status.music_mode is None
        assert len(status.lights) == 2
        assert status.is_on is False and status.is_on == status.lights[0].is_on
        assert (
            status.brightness == 100
            and status.brightness == status.lights[0].brightness
        )
        assert (
            status.color_mode == YeelightMode.ColorTemperature
            and status.color_mode == status.lights[0].color_mode
        )
        assert (
            status.color_temp == 3584
            and status.color_temp == status.lights[0].color_temp
        )
        assert status.rgb is None and status.rgb == status.lights[0].rgb
        assert status.hsv is None and status.hsv == status.lights[0].hsv
        # following are tested in set mode tests
        # assert status.rgb == 16711680
        # assert status.hsv == (359, 100, 100)
        assert (
            status.color_flowing is False
            and status.color_flowing == status.lights[0].color_flowing
        )
        assert (
            status.color_flow_params is None
            and status.color_flow_params == status.lights[0].color_flow_params
        )
        # color_flow_params will be tested after future implementation
        # assert status.color_flow_params == "0,0,1000,1,16711680,100,1000,1,65280,100,1000,1,255,100" and status.color_flow_params == status.lights[0].color_flow_params
        assert status.lights[1].is_on is False
        assert status.lights[1].brightness == 100
        assert status.lights[1].color_mode == YeelightMode.ColorTemperature
        assert status.lights[1].color_temp == 4000
        assert status.lights[1].rgb is None
        assert status.lights[1].hsv is None
        # following are tested in set mode tests
        # assert status.rgb == 15531811
        # assert status.hsv == (65, 86, 100)
        assert status.lights[1].color_flowing is False
        assert status.lights[1].color_flow_params is None
        assert status.moonlight_mode is True
        assert status.moonlight_mode_brightness == 100
