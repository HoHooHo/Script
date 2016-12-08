-- 自动生成文件，请勿手动修改

--_NOTE_
--LT ==== localText
local LT = nil
if _G._TEMP_NAME_Lang then
	LT = _G._TEMP_NAME_Lang.getLang
end

local _TEMP_NAME_ = {
	_TEMP_DATA_
}



local KEYS = {
	_TEMP_KEYS_DATA_
}


local L__TEMP_NAME_ = {}

for k,v in pairs(_TEMP_NAME_) do
	L__TEMP_NAME_[k] = {}
	for k1,v1 in pairs(KEYS) do
		L__TEMP_NAME_[k][k1] = v[v1]
	end
end

-- local getValue = function ( t, id )
-- 	return t[KEYS[id]]
-- end

-- local getKeys = function ()
-- 	return KEYS
-- end

_G._TEMP_NAME__Len = _DATA_LEN
-- _G._TEMP_NAME_ = ReadOnly.readOnly(_TEMP_NAME_, {getValue = getValue, getKeys = getKeys})
_G._TEMP_NAME_ = ReadOnly.readOnly(L__TEMP_NAME_)