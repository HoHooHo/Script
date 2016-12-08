local _TEMP_NAME_ = {}
_TEMP_DATA_
function _TEMP_NAME_.getLang( key, ... )
	return formatLang(_TEMP_NAME_[key], ...)
end
_G._TEMP_NAME_ = ReadOnly.readOnly(_TEMP_NAME_)


