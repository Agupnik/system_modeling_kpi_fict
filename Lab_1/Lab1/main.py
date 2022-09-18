from gen1 import Generator1
from gen2 import Generator2
from gen3 import Generator3


print('\t###__Lambda = 0.5__###')
generator_1 = Generator1(0.5, 10000)
generator_1.analyze(20)
print()

print('\t###__Lambda = 0.3__###')
generator_1 = Generator1(0.3, 10000)
generator_1.analyze(20)
print()

print('\t###__Lambda = 15__###')
generator_1 = Generator1(15, 10000)
generator_1.analyze(20)
print()

print('\t###__Alpha = 2; Sigma = 1__###')
generator_2 = Generator2(2, 1, 10000)
generator_2.analyze(20)
print()

print('\t###__Alpha = 10; Sigma = 5__###')
generator_2 = Generator2(10, 5, 10000)
generator_2.analyze(20)
print()

print('\t###__Alpha = 5; Sigma = 7__###')
generator_2 = Generator2(5, 7, 10000)
generator_2.analyze(20)
print()

print('\t###__A = 5^13; C = 2^31__###')
generator_3 = Generator3(10000, pow(5, 13), pow(2, 31))
generator_3.analyze(20)
print()

print('\t###__A = 5^6; C = 2^15__###')
generator_3 = Generator3(10000, pow(5, 13), pow(2, 31))
generator_3.analyze(20)
print()

print('\t###__A = 5^12; C = 2^10__###')
generator_3 = Generator3(10000, pow(5, 12), pow(2, 10))
generator_3.analyze(20)
print()
