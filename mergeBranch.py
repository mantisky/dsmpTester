#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：定时合并开发版本到测试版本
作者：陈晨
时间：2019-03-28
"""

import os, time, logging

merge_list = [
	{
    	"version":"v1.39",
		"status":True,
		"merge_cycle":5,
		"test_branch":"rel-1.39",
		"dev_branch":["dev-1.39-ip", "dev-1.39-msg"],
		"remark":"合并ip功能和msg功能到测试分支"
	}
]


class MergeBrach():

	def merge(self, merge_list):
		git_list = [
			'git fetch && git checkout {branch} && git pull origin {branch}',
			'git merge origin/{dev_branch} {test_branch}',
			'git push origin {branch}',
			'git status',
			'git merge --abort'
		]

		# 执行合并
		for ii in merge_list:
			test_branch = merge_list['test_branch']
			dev_branch = merge_list['dev_branch']
			try:
				msg_pull = os.popen(git_list[0].format(branch=test_branch))
				msg_merge = os.popen(git_list[2].format(dev_branch=dev_branch, test_branch=test_branch))

			except:
				pass




if __name__ == "__main__":
	merge = MergeBrach()
