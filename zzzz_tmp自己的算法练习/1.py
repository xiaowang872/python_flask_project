from typing import Optional
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        l3=ListNode(0)
        current=l3   #l3为结果链表的头结点,l3.next为结果链表的第一个节点
        jinwei=0    #判断进位
        while l1 or l2 or jinwei:
            if l1:
                l1_tmp=l1.val
            else:
                l1_tmp=0
            if l2:
                l2_tmp=l2.val
            else:
                l2_tmp=0
            total=l1_tmp+l2_tmp+jinwei
            jinwei=total//10  #取整后的商为进位
            current_value=total%10  #取余后的数为当前节点的值
# “%” 运算符：用于取余运算，返回两个数相除的余数。例如，156 % 10 的结果是 6。
# “//” 运算符：用于地板除法，返回两个数相除的结果，向下取整。例如，157 // 10 的结果是 15。
            current.next=ListNode(current_value)  #创建新节点
            current=current.next  #current指向新节点
            if l1:
                l1=l1.next
            if l2:
                l2=l2.next
        return l3.next