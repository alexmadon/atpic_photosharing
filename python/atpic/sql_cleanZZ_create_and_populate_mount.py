#!/usr/bin/python3

out="""
ALTER TABLE storing ADD COLUMN mount char(5);
UPDATE storing SET mount=substring(fastdir_atpic from 0 for 6);
"""
print(out)
