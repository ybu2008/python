# -*- coding:utf-8 -*-
import time
from splinter import Browser

browser = Browser()
loginUrl = 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F'
userNameID = 'TANGRAM__PSP_3__userName'
pwdID = 'TANGRAM__PSP_3__password'
loginBtnID = 'TANGRAM__PSP_3__submit'

signUrl = 'http://zhidao.baidu.com/'
signHrefPath=''
signingHrefText='去签到'
signedHrefText='已签到'
signBtnID='sign-in-btn'

lotteryWndID = 'lucky-machine-wp'
lotteryUrl = 'http://zhidao.baidu.com/shop/lottery'
freeLotteryHrefText = '免费抽奖'

sureText = '确定'


def login():
	
	browser.visit(loginUrl)
	if browser.status_code.is_success():
		browser.find_by_id(userNameID).fill('')
		browser.find_by_id(pwdID).fill('')
		browser.find_by_id(loginBtnID).click()
	else:
		print 'Cannot access websit'
	return

def signIn():
	browser.visit(signUrl)
	time.sleep(5)

	href = browser.find_by_text(signingHrefText)
	# 是否已签到
	if len(href):
		href.click()
		time.sleep(5)
		signBtn = browser.find_by_id(signBtnID)
		if len(signBtn):
			signBtn.click()
	return

def lottery():
	bFlag = true
	waitTime = 600
	browser.visit(lotteryUrl)
	time.sleep(5)

	lotteryWnd = browser.find_by_id(lotteryWndID)
	if 0 == len(lotteryWnd):
		return

	while(true):
		href = lotteryWnd.first.find_by_text(freeLotteryHrefText)
		if 0 != len(href):
			href.click()
			okBtn = lotteryWnd.first.find_by_text(sureText)
			if 0 == len(okBtn):
				return
			else:
				okBtn.click()

		if false == bFlag:
			break

		time.sleep(600)
		bFlag = false
	return

def quit():
	browser.quit()





def splinter(url):
	browser = Browser()
	browser.visit(url)
	time.sleep(5)
	browser.find_by_id(userNameID).fill('')
	browser.find_by_id(pwdID).fill('')
	browser.find_by_id(loginBtnID).click()
	time.sleep(8)
	browser.quit()

# splinter(loginUrl)
login()
time.sleep(3)
signIn()
time.sleep(3)
lottery()
quit()
