import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


class ExecutorManager:
    def __init__(self, max_workers: int):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._DEBUG = False
        self.futures = []

    def submit(self, fn, *args, **kwargs):
        if self._DEBUG:
            future = self.fake_submit(fn, *args, **kwargs)
        else:
            future = self.async_submit(fn, *args, **kwargs)
        self.futures.append(future)

    def async_submit(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def fake_submit(self, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        return FakeFuture(result)

    def results(self, show_progress=False) -> list:
        return list(self.result_iter(show_progress))

    def try_results(self) -> list:
        results = []
        for future in self._wrap_futures():
            try:
                result = future.result()
            except:
                traceback.print_exc()
                result = None
            results.append(result)
        return results

    def result_iter(self, show_progress=False):
        if show_progress:
            for future in tqdm(self._wrap_futures(), total=len(self.futures)):
                yield future.result()
        else:
            for future in self._wrap_futures():
                yield future.result()

    def debug(self):
        self._DEBUG = True
        return self

    def _wrap_futures(self):
        return self if self._DEBUG else as_completed(self.futures)


class FakeFuture:
    def __init__(self, value):
        self.value = value

    def result(self):
        return self.value
