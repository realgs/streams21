def bubble():
    for i in range(len(m)):
        for j in range(len(m)-1):
            if m[j] > m[j+1]:
                temp = m[j]
                m[j] = m[j+1]
                m[j+1] = temp
    return m


def insertion():
    for i in range(len(m)):
        for j in range(i):
            if m[i] < m[j]:
                temp = m[i]
                m[i] = m[j]
                m[j] = temp
    return m
