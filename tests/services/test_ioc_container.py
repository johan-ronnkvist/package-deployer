import pytest
from pkgdeployer.services.ioc_container import IoCContainer


class EnergySource:
    @property
    def capacity(self) -> int:
        raise NotImplementedError()

    def drain(self, amount: int):
        raise NotImplementedError()


class Battery(EnergySource):
    def __init__(self, capacity: int = 20):
        self._capacity = capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    def drain(self, amount: int):
        if self.capacity >= amount:
            self._capacity -= amount
        else:
            raise ValueError("Not enough energy")


class AAABattery(Battery):
    def __init__(self, capacity: int = 20):
        super().__init__(capacity)
        if capacity > 30:
            raise ValueError("AAA batteries can't have more than 30 capacity")


class CarBattery(Battery):
    def __init__(self, capacity: int = 250):
        super().__init__(capacity)
        if capacity > 500:
            raise ValueError("Car batteries can't have more than 500 capacity")


class EnergyConsumer:
    def __init__(self, energy_source: EnergySource):
        self._energy_source = energy_source

    def drain(self, amount: int):
        self._energy_source.drain(amount)


class Flashlight(EnergyConsumer):
    def __init__(self, battery: Battery):
        super().__init__(battery)

    def illuminate(self, lumen: int):
        self.drain(lumen*2)


class TestIoCContainer:
    def test_create_empty_container(self):
        container = IoCContainer()
        assert len(container) == 0

    def test_register_increases_container_size(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        assert len(container) == 1
        assert Battery in container

    def test_container_can_resolve_registered_class_from_factory(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        first = container.resolve(Battery)
        second = container.resolve(Battery)
        assert isinstance(first, AAABattery)
        assert first is not second

    def test_container_can_resolve_registered_class_with_kwargs(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        instance = container.resolve(Battery, capacity=25)
        assert isinstance(instance, AAABattery)
        assert instance.capacity == 25

    def test_container_can_resolve_dependencies(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        container.register(EnergyConsumer, Flashlight)
        instance = container.resolve(EnergyConsumer)
        assert isinstance(instance, Flashlight)
        assert isinstance(instance._energy_source, AAABattery)

    def test_container_can_register_instance(self):
        container = IoCContainer()
        container.register(Battery, AAABattery(capacity=25))
        first = container.resolve(Battery)
        second = container.resolve(Battery)
        assert first is second
        first.drain(10)
        assert first.capacity == 15
        assert second.capacity == 15

    def test_unregister(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        assert len(container) == 1

        container.unregister(Battery)
        assert len(container) == 0
        assert Battery not in container

    def test_unregister_nonexistent_key(self):
        container = IoCContainer()
        with pytest.raises(KeyError):
            container.unregister(Battery)

    def test_clear(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        container.register(EnergyConsumer, Flashlight)
        assert len(container) == 2

        container.clear()
        assert len(container) == 0

    def test_contains(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        container.register(EnergyConsumer, Flashlight)

        assert Battery in container
        assert EnergyConsumer in container
        assert CarBattery not in container

    def test_len(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        container.register(EnergyConsumer, Flashlight)
        container.register(CarBattery, CarBattery)

        assert len(container) == 3

    def test_resolve_missing_dependency(self):
        container = IoCContainer()
        container.register(Battery, AAABattery)
        container.register(EnergyConsumer, Flashlight)

        with pytest.raises(KeyError):
            container.resolve(CarBattery)

    def test_resolve_instance_with_kwargs_raises_type_error(self):
        container = IoCContainer()
        instance = AAABattery(capacity=25)
        container.register(Battery, instance)

        with pytest.raises(TypeError):
            container.resolve(Battery, capacity=30)

    def test_resolve_instance_with_invalid_kwargs(self):
        container = IoCContainer()
        instance = AAABattery(capacity=25)
        container.register(Battery, instance)

        with pytest.raises(TypeError):
            container.resolve(Battery, invalid_kwarg=42)
