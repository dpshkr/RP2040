from uctypes import addressof

angles = bytearray(b'\xdb\x0f\xc9\x00\x9c\xb1v\x00\xec\xb6>\x00\xbb\xd5\x1f\x00\xae\xfa\x0f\x00U\xff\x07\x00\xeb\xff\x03\x00\xfd\xff\x01\x00\x00\x00\x01\x00\x00\x80\x00\x00\x00@\x00\x00\x00 \x00\x00\x00\x10\x00\x00\x00\x08\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x80\x00\x00\x00@\x00\x00\x00 \x00\x00\x00\x10\x00\x00\x00\x08\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00')

@micropython.asm_thumb
def cos(r0,r1,r2):
    # r0 = alpha
    # r1 = Number of iterations
    # r2 = address of the atan table
    # r3 = x
    # r4 = y
    # r5 = loop counter
    # r6 = theta
    # r7 = scratch
    mov(r3,1) # Move 1 into x = r3
    mov(r4,24)
    lsl(r3,r4)
    mov(r4,0) # Move 4 into y = r4
    mov(r5,0) # i = r5 Loop counter
    mov(r6,0) # theta = 0
    
    label(LOOP)
    ldr(r7, [r2,0]) # Load the angle into r7 = tan-1
    cmp(r0, r6)
    
    blt(LESSTHAN)
    push({r6,r7})
    mov(r6,r3) # r6 = x
    asr(r6,r5) # r6 = x>>i
    mov(r7,r4) # r7 = y
    asr(r7,r5) # r7 = y>>i
    sub(r3,r3,r7) # x = x - y>>i
    add(r4,r4,r6) # y = y + x>>i
    pop({r6,r7})
    add(r6, r6, r7) # theta = theta + tan^-1
    b(END)
    
    label(LESSTHAN)
    push({r6,r7})
    mov(r6,r3) # r6 = x
    asr(r6,r5) # r6 = x>>i
    mov(r7,r4) # r7 = y
    asr(r7,r5) # r7 = y>>i
    add(r3,r3,r7) # x = x + y>>i
    sub(r4,r4,r6) # y = y - x>>i
    pop({r6,r7})
    sub(r6, r6, r7) # theta = theta - tan^-1
    label(END)
    
    add(r5,r5,1)
    add(r2,r2,4)
    cmp(r5,r1)
    bne(LOOP)
    
    mov(r0,r3)
