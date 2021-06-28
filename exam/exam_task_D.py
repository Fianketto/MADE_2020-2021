error_close = 0
error_open = 0
open_mem = ""
close_mem = ""

# inp = ['<X>', '<Y>', '</Y>', '</X>', '<AA>', '<AA>', '<Z>', '</Z>']
# inp_len = len(inp)

set_count = int(input())
ans = ["" for i in range(set_count)]
for set_n in range(set_count):
    inp_len = int(input())
    inp = []
    for i in range(inp_len):
        inp_str = input()
        inp.append(inp_str.upper())

    # 1. CLOSING IS error
    tags_stack = []
    tag_count = 0
    for tag in inp:
        # print("now tag is ", tag)
        if tag[1] != '/':
            # print("opening -> into stack")
            tags_stack.append(tag)
            tag_count += 1
        else:
            # print("its closing")
            if tag_count > 0:
                prev_tag = tags_stack[tag_count - 1]
                if prev_tag[1:-1] == tag[2:-1]:
                    # print("ok, closing last open")
                    del tags_stack[tag_count - 1]
                    tag_count -= 1
                else:
                    # print("close doesnt match")
                    error_close += 1
                    close_mem = tag
            else:
                error_close += 1
                close_mem = tag

    if tag_count > 0:
        error_close += tag_count
        close_mem = tags_stack[tag_count - 1]

    # 2. OPENING IS error
    tags_stack = []
    tag_count = 0
    for tag in inp:
        # print("now tag is ", tag)
        if tag[1] != '/':
            # print("opening -> into stack")
            tags_stack.append(tag)
            tag_count += 1
        else:
            # print("its closing")
            if tag_count > 0:
                prev_tag = tags_stack[tag_count - 1]
                if prev_tag[1:-1] == tag[2:-1]:
                    # print("ok, closing last open")
                    del tags_stack[tag_count - 1]
                    tag_count -= 1
                else:
                    # print("close doesnt match")
                    error_open += 1
                    open_mem = prev_tag
                    del tags_stack[tag_count - 1]
                    tag_count -= 1
                    # print("trying to match previous")
                    if tag_count > 0:
                        prev_tag = tags_stack[tag_count - 1]
                        if prev_tag[1:-1] == tag[2:-1]:
                            # print("ok, closing previous open")
                            del tags_stack[tag_count - 1]
                            tag_count -= 1
                        else:
                            # print("close doesnt match AGAIN")
                            error_open += 1
                    else:
                        error_open += 1
            else:
                error_open += 1
                open_mem = tag

    if tag_count > 0:
        error_open += tag_count
        open_mem = tags_stack[tag_count - 1]

    if error_close <= error_open:
        if error_close == 0:
            ans[set_n] = "CORRECT"
        elif error_close == 1:
            ans[set_n] = "ALMOST " + close_mem
        else:
            ans[set_n] = "INCORRECT"
    else:
        if error_open == 0:
            ans[set_n] = "CORRECT"
        elif error_open == 1:
            ans[set_n] = "ALMOST " + open_mem
        else:
            ans[set_n] = "INCORRECT"

    # if inp_len < 2:
    #    ans[set_n] = "INCORRECT"

#    print(ans[set_n])

for set_n in range(set_count):
    print(ans[set_n])
