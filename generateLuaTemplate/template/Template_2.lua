-- 自动生成文件，请勿手动修改

--_NOTE_
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

return {data = ReadOnly.readOnly(L__TEMP_NAME_), len = _DATA_LEN}