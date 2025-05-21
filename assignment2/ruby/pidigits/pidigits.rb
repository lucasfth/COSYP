# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# contributed by Gabriele Renzi

class PiDigitSpigot
  def initialize
    @z = Transformation.new 1, 0, 0, 1
    @x = Transformation.new 0, 0, 0, 0
    @inverse = Transformation.new 0, 0, 0, 0
  end

  def next!
    @y = @z.extract(3)
    if safe? @y
      @z = produce(@y)
      @y
    else
      @z = consume @x.next!
      next!
    end
  end

  def safe?(digit)
    digit == @z.extract(4)
  end

  def produce(i)
    @inverse.qrst(10, -10 * i, 0, 1).compose(@z)
  end

  def consume(a)
    @z.compose(a)
  end
end

class Transformation
  attr_reader :q, :r, :s, :t

  def initialize(q, r, s, t)
    @q = q
    @r = r
    @s = s
    @t = t
    @k = 0
  end

  def next!
    @q = @k += 1
    @r = 4 * @k + 2
    @s = 0
    @t = 2 * @k + 1
    self
  end

  def extract(j)
    (@q * j + @r) / (@s * j + @t)
  end

  def compose(a)
    self.class.new(@q * a.q,
                   @q * a.r + r * a.t,
                   @s * a.q + t * a.s,
                   @s * a.r + t * a.t)
  end

  def qrst *args
    initialize(*args)
    self
  end
end
