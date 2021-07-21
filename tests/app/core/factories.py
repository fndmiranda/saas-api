import asyncio
import inspect

import factory

from app.database import async_session

factory.Faker._DEFAULT_LOCALE = "pt_BR"


class BaseFactory(factory.Factory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            for key, value in kwargs.items():
                # when using SubFactory, you'll have a Task in the
                # corresponding kwarg await tasks to pass model
                # instances instead
                if inspect.isawaitable(value):
                    kwargs[key] = await value

            async with async_session() as session:
                # replace as needed by your way of creating model instances
                instance = model_class(*args, **kwargs)
                session.add(instance)
                await session.commit()
                return instance

        # A Task can be awaited multiple times, unlike a coroutine.
        # useful when a factory and a subfactory must share a same object
        return asyncio.create_task(maker_coroutine())

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            return model_class(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]
