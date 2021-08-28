
import asyncio
import multiprocessing

class Pipeline():

  def __init__(self, funcs=[], id=None):
    self.functions = funcs
    self.id = idd

  def __or__(self, callback):
    if callable(callback):
      self.functions += [callback]
    else:
      raise TypeError(f'{type(callback).__name__} is not callable')

  """
    Egg = object that implements __aiter__
    if Egg is none, use first function as input
  """
  async def __acall__(self, egg=None):
    async for i in self.functions[0](self.id):
      result = i
      for func in self.functions:
        result = func(result)

  def __run_acall__(self):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.__acall__(self.input))

  def __call__(self):
    self.input = self.input 
    process = multiprocessing.Process(target=self.__run_acall__)
    process.start()

  def __repr__(self):
    return f'{type(self)} {[s.__name__ for s in self.functions]}'

class MakePipeline():

  def __or__(self, function):
    return Pipeline([function])

pype = MakePipeline()

class PQueue():
  class StopProxy:
    pass
  End = StopProxy()
  
  def __init__(self, manager):
    self.queue = manager.Queue()
  
  # For use by user

  def __lt__(self, item):
    """
      Allows the user to chain add stuff.
      PQueue < 'hi' < 1 < 'bye'
    """
    self.queue.put(item)
    return self
  
  # TODO: Rework this with pass by ref
  def __gt__(self, item):
    """
      Blocking read
      hi = [0]
      PQueue > hi
      print(hi) # prints some other value
    """
    item[0] = self.queue.get()
    return self

  def __add__(self, item):
    self.queue.put(item)
    return item

  # For use in pipelines
  def __pos__(self):
    """
      Allows pipeline to put stuff into this PQueue
      do_stuff = increment | +PQueue | print
    """
    return self.__add__

  def __neg__(self):
    """
      do_stuff = -PQueue | print
    """
    # return Pipeline([], self) 
    # ^^^ test which one is better
    return Pipeline([self.__aiter__])

  def end(self):
    self.queue.put(PQueue.End)

  async def __aiter__(self):
    """
    Not thread safe
    """
    while True:
      item = self.queue.get()
      if item == PQueue.StopProxy:
        self.queue._close
        return
      yield item
  

class Egg(PQueue):
  
  manager = multiprocessing.Manager()

  def __init__(self):
    import atexit
    super().__init__(Egg.manager)
    atexit.register(self.end)

  def 

  
if __name__ == '__main__':

  def increment(n):
    return n + 1

  def double(n):
    return n * 2

  a, b, c = Egg(), Egg(), Egg()
  int_compute = -a | +b | increment | double | print 


  # this is current syntax, too verbose 
  blur_image = -image | blur_operation
  my_blur = blur_image | +blur1 | +blur2
  blur_black_white_image = -blur1 | black_and_white
  blur_sepia_image = -blur2 | sepia 

  # this is what we want
  blur_black = blur_image | black_and_white 
  blur_serpa = blur_image | sepia