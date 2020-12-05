# -*-coding:utf-8-*-
class HaiMing:
    def __init__(self, verification_flag=1):
        # 设置奇偶校验 1为奇校验 0 为偶校验
        self.verification_flag = verification_flag
        # 最大的检验码位数
        self.max_check_bit = 12

    # 对将要编码为海明码的二进制计算校验码的位数
    def compute_p_num_1(self, data):
        # 2**p >= m+p+1
        for p in range(1, self.max_check_bit):
            if 2 ** p >= len(data) + p + 1:
                return p

    # 对接收到的海明码计算校验码位数
    def compute_p_num_2(self, data):
        # 2**p >= m+p+1
        for p in range(1, self.max_check_bit):
            if 2 ** p >= len(data) + 1:  # len(data) = m + p
                return p

    # 按校验位顺序确定约束数据位索引二进制
    def get_check_code_index_group(self, binary_code):
        check_code_index_group = []
        for k in range(1, self.p_num + 1):
            temp = []
            for b in binary_code:
                try:
                    if b[-k] == "1":
                        temp.append(b)
                except:
                    pass
            check_code_index_group.append(temp)
        return check_code_index_group # [['11', '101', '111'], ['11', '110', '111'], ['101', '110', '111']]

    # 获取二进制索引对应位的值
    def get_check_code_group(self, code_table, check_code_index_group):
        check_code_group = []
        for i in check_code_index_group:
            temp = []
            for j in i:
                e = int(j, 2)
                temp.append(code_table[e - 1])
            check_code_group.append(temp)
        return check_code_group # [['1', '0', '0'], ['1', '1', '0'], ['0', '1', '0']]

    # 生成或计算校验码
    def verify(self, check_code_group):
        p_group = []
        for i in check_code_group:
            one_num = i.count("1")
            if one_num % 2 == self.verification_flag:
                p_group.append(0)
            else:
                p_group.append(1)
        return p_group # [0, 1, 0]

    # 将二进制编码为海明码
    def encode(self, data):
        self.p_num = self.compute_p_num_1(data)
        code_table = list(data)
        p_index = []
        for i in range(self.p_num):
            code_table.insert(2 ** i - 1, None)
            p_index.append(2 ** i - 1)

        # 将索引转为二进制形式
        binary_code = []
        for j in range(1, len(code_table) + 1):
            if j - 1 not in p_index:
                binary_code.append(bin(j).replace("0b", ""))

        check_code_index_group = self.get_check_code_index_group(binary_code)
        check_code_group = self.get_check_code_group(code_table, check_code_index_group)
        p_group = self.verify(check_code_group)

        # 填充码表
        new_code_table = list(data)
        for i, j in zip(p_index, p_group):
            new_code_table.insert(i, j)

        new_code_table = list(map(lambda x: str(x), new_code_table))
        return "".join(new_code_table)

    # 检测错误位
    def check(self, data):
        code_table = list(data)
        self.p_num = self.compute_p_num_2(data)

        # 将索引转为二进制形式
        binary_code = []
        for j in range(1, len(code_table) + 1):
            binary_code.append(bin(j).replace("0b", ""))

        check_code_index_group = self.get_check_code_index_group(binary_code)
        check_code_group = self.get_check_code_group(code_table, check_code_index_group)

        p_group = self.verify(check_code_group)
        p_group.reverse()

        check_result = list(map(lambda x: str(x), p_group))
        check_result = "".join(check_result)
        return check_result

    # 自动纠错
    def correct(self, data):
        result = self.check(data)
        error_value_index = len(data) - int(result, 2)
        correct_value = int(data, 2) ^ (1 << error_value_index)
        return bin(correct_value).replace("0b", "").zfill(len(data))


if __name__ == '__main__':

    hm = HaiMing()

    print(hm.encode("1010"))  # 编码为海明码 1010 -> 0110010

    print(hm.check("0110000"))  # 二进制110 = 十进制6 可以得知 0110010 从左到右第6位出错

    print(hm.correct("0110000"))  # 自动纠错 0110000 -> 0110010
