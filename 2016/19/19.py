import common


def weparty(nums):
    if not isinstance(nums, list):
        nums = [i+1 for i in range(nums)]
    if len(nums) == 1:
        return nums[0]
    if len(nums) % 2 == 0:
        # if even, then just take out "every second"
        return weparty(nums[::2])
    else:
        # if odd, then take out "every second" and remove first
        return weparty(nums[::2][1:])


def cirle_party(nums):
    if not isinstance(nums, list):
        nums = [i + 1 for i in range(nums)]

    while len(nums) > 5:
        print(nums)
        tl = (len(nums) * 2) // 3
        fl = (len(nums) + 2) // 3
        if len(nums) % 2 == 0:
            ml = (fl // 2) + 1
            ll = (fl // 2) - 1
            if fl + ll + ml > tl:
                ml -= 1
                ll -= 1
            nums = nums[fl:fl+ll] + nums[fl+ll::3][:ml] + nums[:fl]
        else:
            ml = (fl // 2) + 1
            ll = (fl // 2)
            if fl + ll + ml > tl:
                ml -= 1
                ll -= 1
            nums = nums[fl:fl + ll] + nums[fl + ll + 1::3][:ml] + nums[:fl]

    while len(nums) > 1:
        print(nums)
        nums = nums[1:len(nums) // 2] + nums[len(nums) // 2 + 1:] + [nums[0]]
    return nums[0]

assert weparty(5) == 3
assert weparty(7) == 7
assert weparty(13) == 11
assert weparty(10) == 5

print(f"WE Party won elf {weparty(common.Loader.load_lines(numeric=True)[0])}")

assert cirle_party(5) == 2
assert cirle_party(7) == 5
assert cirle_party(13) == 4
assert cirle_party(10) == 1

print(f"Cirlce Party won elf {cirle_party(common.Loader.load_lines(numeric=True)[0])}")