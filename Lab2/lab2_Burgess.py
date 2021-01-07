
# 1st task of lab2 - Fall 2020
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

# 0 * something is 0
# 1 * something is something

# while loop (optional)
# what is the 1st index of a list? 0 -> part1[0] -> 1
# what us the last index of a list? suppose the length of this list is n -> n-1; part1[12] -> 4096 
# i > 0, 1, 2, 3, ..., 12 part1[13] -> error message: out of index bound

# result1 = 1
# i = 0
# n_length = 13

# while i < n_length:  
#     result1 = result1 * part1[i] 
#     i = i + 1
# print('fdsasdfghjhgfds')

# for loop
result1 = 1
for i in part1:
    result1 = result1 * i         

# if we define part1 as [8, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
#1st: i is 8, anti is 8; "result1 = result1 * i " <- "8 = result1 * 8" <- "result1 should be one at the very first time"
#2nd: i is 2, anti is 8 * 2 = 16
#3rd: i is 4, anti is 8 * 2 * 4 = 64 
# ........................................

print('The result of 1st task is:', result1)

########################################################################

# 2nd task of lab2- Fall 2020
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]

# 0 + something is something ('something' is not changed)
# 1 + something is something + 1 ('something' is changed)

result2 = 0 # 1 is not correct, 0 is correct
for i in part2:
    result2 = result2 + i

# if we define part2 as [8, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
#1st: i is 8, anti is 8; "result1 = result1 * i " <- "8 = result1 + 8" <- "result1 should be one at the very first time"
#2nd: i is 2, anti is 8 + 2 = 10
#3rd: i is 4, anti is (8 + 2) + 4 = 14 
# ........................................

print('The result of 2nd task is:', result2)

########################################################################

# 3rd task of lab2 - Fall 2020
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 

result3 = 0
for i in part3:
    if i%2 == 0:
        result3 = result3 + i

print('The result of 3rd task is:', result3)