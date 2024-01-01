# RESTful APIs (2023/12)

## List Medical Facilities (with specific type)

### [GET] `/med_facility/basic_info`
Get medical facility basic information.
* Facility id (defined by NHI)
* Name
* Facility Type
* Phone
* Address
* Remarks

### Parameters
`type` (required)

#### Valid Options
- medical_center
- regional_hospital
- district_hospital
- small_clinic

`id` (required) -> The medical facility id defined by NHI.

### Request (example)
`/med_facility/basic_info?type=medical_center&id=0401180014`

### Response (example)

<details>
    <summary>Expand</summary>
    
```json
{
    "status": "success",
    "data": {
        "site_id": "0401180014",
        "site_name": "國立臺灣大學醫學院附設醫院",
        "site_type": "醫學中心",
        "site_telephone": "02-23123456",
        "site_address": "臺北市中正區中山南路7、8號；常德街1號",
        "site_remark": "急診全年無休，24小時提供服務；西址院區周六未開診，部分診改至兒醫大樓"
    }
}
```
 
</details>

***

### [GET] `/med_facility/count`
Count the medical facility with specific type.

### Parameters
`type` (required)

#### Valid Options
- medical_center
- regional_hospital
- district_hospital
- small_clinic

### Request (example)
`/med_facility/count?type=small_clinic`

### Response (example)

```json
{
    "status": "success",
    "data": {
        "total_count": 24222
    }
}
```
***

### [GET] `/med_facility/list`
Get the full medical facility list of specific type.

### Parameters
`type` (required)

#### Valid Options
- medical_center
- regional_hospital
- district_hospital
- small_clinic

### Request (example)
`/med_facility/list?type=medical_center`

### Response (example)

<details>
    <summary>Expand</summary>

```json
{
    "status": "success",
    "data": {
        "total_count": 25,
        "items": [
            {
                "site_id": "1142100017",
                "site_name": "長庚醫療財團法人高雄長庚紀念醫院",
                "site_type": "醫學中心",
                "site_telephone": "07-7317123",
                "site_address": "高雄市鳥松區大埤路123號",
                "site_region_lv1": "高雄市",
                "site_region_lv2": "鳥松區",
                "site_service_list": [
                    "復健－物理治療業務",
                    "復健－職能治療業務",
                    "住院安寧療護",
                    "復健－語言治療業務",
                    "門診診療",
                    "住院診療",
                    "血液透析",
                    "兒童預防保健",
                    "成人預防保健",
                    "婦女子宮頸抹片檢查",
                    "孕婦產檢",
                    "分娩",
                    "精神病患者居家照護",
                    "義肢業務",
                    "兒童牙齒預防保健",
                    "婦女乳房檢查",
                    "精神科日間住院治療",
                    "腹膜透析業務",
                    "口腔黏膜檢查",
                    "定量免疫法糞便潛血檢查"
                ],
                "site_function_list": [
                    "不分科",
                    "家醫科",
                    "內科",
                    "外科",
                    "兒科",
                    "婦產科",
                    "骨科",
                    "神經外科",
                    "泌尿科",
                    "耳鼻喉科",
                    "眼科",
                    "皮膚科",
                    "神經科",
                    "精神科",
                    "復健科",
                    "整形外科",
                    "職業醫學科",
                    "急診醫學科",
                    "牙科",
                    "牙體復形科",
                    "牙髓病科",
                    "齒顎矯正科",
                    "兒童牙科",
                    "口腔顎面外科",
                    "口腔病理科",
                    "中醫一般科",
                    "麻醉科",
                    "核子醫學科",
                    "放射腫瘤科",
                    "放射診斷科",
                    "解剖病理科",
                    "臨床病理科"
                ],
                "site_working_hours": {
                    "Monday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Tuesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Wednesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Thursday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Friday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Saturday": {
                        "morning": "Y",
                        "afternoon": "N",
                        "evening": "N"
                    },
                    "Sunday": {
                        "morning": "N",
                        "afternoon": "N",
                        "evening": "N"
                    }
                },
                "site_remark": "本院急診室提供全天24小時急診醫療服務"
            },
            ...
            ...
}
```

</details>

***

### [GET] `/med_facility/list_by_division`
Get a medical facility list of specific type with a given division name.

### Parameters
`type` (required)

#### Valid Options
- medical_center
- regional_hospital
- district_hospital
- small_clinic

`division` (required)

#### Valid Options
The city or county names (the first level) and the sections or townships names (the second level) in Taiwan.
It will support value like: `台北市` or `台北市大安區`, only if the given values exists. (names will be verified).

More examples:
- `台中市西區` is valid
- `花蓮縣大安區` is invalid (no such township or section in 花蓮縣)
- `高雄縣` is invalid (the old city / county name is not supported)

### Request (example)
`/med_facility/list_by_division?type=medical_center&division=臺北市大安區`

### Response (example)

<details> 
    <summary>Expand</summary>

```json

{
    "status": "success",
    "data": {
        "total_count": 1,
        "items": [
            {
                "site_id": "1101020018",
                "site_name": "國泰醫療財團法人國泰綜合醫院",
                "site_type": "醫學中心",
                "site_telephone": "02-27082121",
                "site_address": "臺北市大安區仁愛路4段280號，266巷6號",
                "site_region_lv1": "臺北市",
                "site_region_lv2": "大安區",
                "site_service_list": [
                    "復健－物理治療業務",
                    "復健－職能治療業務",
                    "復健－語言治療業務",
                    "門診診療",
                    "住院診療",
                    "血液透析",
                    "兒童預防保健",
                    "成人預防保健",
                    "婦女子宮頸抹片檢查",
                    "孕婦產檢",
                    "分娩",
                    "義肢業務",
                    "兒童牙齒預防保健",
                    "結核病",
                    "口腔黏膜檢查",
                    "定量免疫法糞便潛血檢查"
                ],
                "site_function_list": [
                    "不分科",
                    "家醫科",
                    "內科",
                    "外科",
                    "兒科",
                    "婦產科",
                    "骨科",
                    "神經外科",
                    "泌尿科",
                    "耳鼻喉科",
                    "眼科",
                    "皮膚科",
                    "神經科",
                    "精神科",
                    "復健科",
                    "整形外科",
                    "職業醫學科",
                    "急診醫學科",
                    "牙科",
                    "牙髓病科",
                    "牙周病科",
                    "齒顎矯正科",
                    "兒童牙科",
                    "口腔顎面外科",
                    "家庭牙醫科",
                    "麻醉科",
                    "核子醫學科",
                    "放射腫瘤科",
                    "放射診斷科",
                    "解剖病理科",
                    "臨床病理科"
                ],
                "site_working_hours": {
                    "Monday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Tuesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Wednesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Thursday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Friday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Saturday": {
                        "morning": "Y",
                        "afternoon": "N",
                        "evening": "N"
                    },
                    "Sunday": {
                        "morning": "N",
                        "afternoon": "N",
                        "evening": "N"
                    }
                },
                "site_remark": "急診全年無休，24小時提供服務"
            }
        ]
    }
}

```

</details>

***

### [GET] `/med_facility/count_by_division`
Count the specific medical facility with a given division name.

### Parameters
`type` (required)

#### Valid Options
- medical_center
- regional_hospital
- district_hospital
- small_clinic

`division` (required)

#### Valid Options
The city or county names (the first level) and the sections or townships names (the second level) in Taiwan.
It will support value like: `台北市` or `台北市大安區`, only if the given values exists. (names will be verified).

More examples:
- `台中市西區` is valid
- `花蓮縣大安區` is invalid (no such township or section in 花蓮縣)
- `高雄縣` is invalid (the old city / county name is not supported)

### Request (example)
`/med_facility/count_by_division?type=small_clinic&division=臺北市大安區`

### Response (example)

```json
{
    "status": "success",
    "data": {
        "total_count": 603
    }
}
```
***


## Search Medical Facilities
### [POST] `/med_facility/search`
Search the medical facility with variety of search keys.

### Paremeters

`type` (required)

Should be a list of facility types, provide at least 1 type. Valid options are:
- medical_center
- regional_hospital
- district_hospital
- small_clinic

`function` (optional)

Should be a list of medical department or function. Some examples are:
- 外科
- 內科
- 骨科
- 皮膚科

`division` (optional)

The city or county names (the first level) and the sections or townships names (the second level) in Taiwan.
It will support value like: `台北市` or `台北市大安區`, only if the given values exists. (names will be verified).

More examples:
- `台中市西區` is valid
- `花蓮縣大安區` is invalid (no such township or section in 花蓮縣)
- `高雄縣` is invalid (the old city / county name is not supported)

`keyword` (optional)

The full or partial name of the medical facility.

### Request (example)

`/med_facility/search`

(JSON formatted request body)

```json
{
    "type": [
        "medical_center",
        "regional_hospital",
        "district_hospital"
    ],
    "division": "臺中市",
    "keyword": "榮民"
}
```

### Response (example)

<details>
    <summary>Expand</summary>

```json
{
    "status": "success",
    "data": {
        "total_count": 1,
        "items": [
            {
                "site_id": "0617060018",
                "site_name": "臺中榮民總醫院",
                "site_type": "醫學中心",
                "site_telephone": "04-23592525",
                "site_address": "臺中市西屯區臺灣大道4段 1650號",
                "site_region_lv1": "臺中市",
                "site_region_lv2": "西屯區",
                "site_service_list": [
                    "復健－物理治療業務",
                    "復健－職能治療業務",
                    "住院安寧療護",
                    "復健－聽力檢查業務",
                    "復健－語言治療業務",
                    "門診診療",
                    "住院診療",
                    "血液透析",
                    "兒童預防保健",
                    "成人預防保健",
                    "婦女子宮頸抹片檢查",
                    "孕婦產檢",
                    "分娩",
                    "精神病患者居家照護",
                    "義肢業務",
                    "兒童牙齒預防保健",
                    "婦女乳房檢查",
                    "精神科日間住院治療",
                    "腹膜透析業務",
                    "口腔黏膜檢查",
                    "定量免疫法糞便潛血檢查"
                ],
                "site_function_list": [
                    "不分科",
                    "家醫科",
                    "內科",
                    "外科",
                    "兒科",
                    "婦產科",
                    "骨科",
                    "神經外科",
                    "泌尿科",
                    "耳鼻喉科",
                    "眼科",
                    "皮膚科",
                    "神經科",
                    "精神科",
                    "復健科",
                    "整形外科",
                    "職業醫學科",
                    "急診醫學科",
                    "牙科",
                    "牙髓病科",
                    "牙周病科",
                    "復補綴牙科",
                    "齒顎矯正科",
                    "兒童牙科",
                    "口腔顎面外科",
                    "口腔病理科",
                    "特殊需求者口腔醫學科",
                    "中醫一般科",
                    "麻醉科",
                    "核子醫學科",
                    "放射腫瘤科",
                    "放射診斷科",
                    "解剖病理科",
                    "臨床病理科"
                ],
                "site_working_hours": {
                    "Monday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Tuesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Wednesday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Thursday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Friday": {
                        "morning": "Y",
                        "afternoon": "Y",
                        "evening": "Y"
                    },
                    "Saturday": {
                        "morning": "Y",
                        "afternoon": "N",
                        "evening": "N"
                    },
                    "Sunday": {
                        "morning": "N",
                        "afternoon": "N",
                        "evening": "N"
                    }
                },
                "site_remark": "本院提供24小時提供急診服務"
            }
        ]
    }
}
```

</details>

***

## Unfinished or experimental
* /med_facility/working_hours

## Upcoming / Todo list
* Frontend integration with Grafana dashboards
* Add more web APIs for data displaying
* Provide swagger.json
* Cloud deployment (APP Engine + MangoDB Atlas)
