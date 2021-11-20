from numpy.fft import fft, ifft

number_to_list = lambda n: list(map(lambda x: int(x), reversed(list(str(n)))))
addition = lambda X, Y: [X[i] + Y[i] for i in range(len(X))]
multiplication = lambda X, Y: [X[i] * Y[i] for i in range(len(X))]

def convolve(X, Y, operation):
  (X, Y) = map(lambda x: fft(x), (X, Y))
  z = operation(X, Y)
  z = ifft(z)
  return list(map(lambda x: int(x.real + 0.5), z))

def process_digits(X, Y, operation):
  n = 1 << max(len(X), len(Y))
  (X, Y) = map(lambda x: x + [0] * (n - len(x)), (X, Y))
  z = convolve(X, Y, operation)
  while z[-1] == 0: z.pop()
  res, carry = [], 0
  for x in z:
    carry += x
    res.append(int(carry) % 10)
    carry /= 10
  if carry: res.append(int(carry))
  return res

def perform_operation(x, y, operation):
  if not all([isinstance(x, int) for x in (x, y)]):
    return 'Arguments should be integers'
  if not all([x >= 0 for x in (x, y)]):
    return 'Arguments should not be negative'
  (X, Y) = map(lambda x: number_to_list(x), (x, y))
  Z = process_digits(X, Y, operation)
  return int(''.join(map(lambda x: str(x), reversed(Z))))

fft_add = lambda x, y: (
  perform_operation(x, y, addition) if any(x != 0 for x in (x, y)) else 0
)
fft_multiply = lambda x, y: (
  perform_operation(x, y, multiplication) if all(x != 0 for x in (x, y)) else 0
)
def fft_pow(x, y):
  if y == 0: return 1
  if x == 0: return 0
  r = 1
  for _ in range(y): r = fft_multiply(r, x)
  return r
