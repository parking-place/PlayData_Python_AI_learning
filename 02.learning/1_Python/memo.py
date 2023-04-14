
file_name = input('파일 이름을 입력하세요: ')
file_extension = 'txt'

if file_name == None:
    file_name = 'memo'
elif len(file_name.split('.')) > 2:
    file_extension = file_name.split('.')[-1]
    file_name = file_name.split('.')[0]

print(f'file_name: {file_name}.{file_extension}')

lines = []
with open(f'.\\iotest\\{file_name}.{file_extension}', 'wt', encoding='utf-8') as memo:
    while True:
        line = input('메모를 입력하세요: ')
        if line == '!q':
            break
        lines.append(line + '\n')
        # print(f'입력 :{line}')
    memo.writelines(lines)
    
with open(f'.\\iotest\\{file_name}.{file_extension}', 'rt', encoding='utf-8') as memo:
    for i, t in enumerate(memo, start=1):
        print(f'{i:2d} |{t}', end='')
