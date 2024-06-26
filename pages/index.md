---
title: Redfin Real Estate Report
---

```sql get_min_max_period_end

    SELECT 
    CAST(MAX(period_end) AS DATE) as "max_date",
    CAST(MIN(period_end) AS DATE) as "min_date"
    FROM median_sale_price_per_state
```
Period from <Value data={get_min_max_period_end} column=min_date /> to <Value data={get_min_max_period_end} column=max_date />


## Select a State and Property Type to View Data

```sql states
  select
      state
  from median_sale_price_per_state
  group by state
```

<Dropdown
    name=state
    data={states}
    value=state
    title="Select a State"
>
    <DropdownOption value="United States"/>
</Dropdown>


```sql property_types
  select
      property_type
  from median_sale_price_per_state
  group by property_type 
```


<ButtonGroup
    data={property_types} 
    name=Property_Types
    value=property_type
    defaultValue="Single Family Residential"
    title="Select a Property Type"
>
    <!-- <ButtonGroupItem valueLabel="All Categories" value="%" default /> -->
    <!-- <ButtonGroupItem valueLabel="Single Family Residential" value=' default /> -->
</ButtonGroup>


```sql top_20_median_sale_price
SELECT state,
median_sale_price,
property_type

FROM combined_price_homes_sold
WHERE state not in ('United States','Columbia')
AND property_type like '${inputs.Property_Types}'
ORDER BY median_sale_price DESC
Limit 20
```


<BarChart 
    data={top_20_median_sale_price} 
    x=state
    y=median_sale_price
    title="Top 20 States With The Highest Median Sale Price By Property Type Latest Period"
/>

```sql bottom_20_median_sale_price
SELECT state,
median_sale_price,
property_type

FROM combined_price_homes_sold
WHERE state not in ('United States','Columbia')
AND property_type like '${inputs.Property_Types}'
ORDER BY median_sale_price ASC
Limit 20
```

<BarChart 
    data={bottom_20_median_sale_price}
    x=state
    y=median_sale_price
    sort=false
    title="Top 20 States With The Lowest Median Sale Price By Property Type Latest Period"
/>

```sql median_sale_price_by_state
    SELECT * FROM median_sale_price_per_state
    WHERE state LIKE '${inputs.state.value}'
    AND property_type like '${inputs.Property_Types}'
```


<LineChart data={median_sale_price_by_state} x=period_end y=median_sale_price yAxisTitle="Median Sale Price" title="Selected State Median Sale Price">
    <ReferenceLine x='2020-03-11' label="Start Covid Pandemic" hideValue=true/>
    <ReferenceLine x='2023-05-05' label="End Covid Pandemic" hideValue=true/>
</LineChart>


```sql median_ppsf_per_state
    SELECT * FROM median_ppsf_per_state
    WHERE state LIKE '${inputs.state.value}'
    AND property_type like '${inputs.Property_Types}'
```



<LineChart data={median_ppsf_per_state} x=period_end y=median_ppsf yAxisTitle="Median Price Per Square Foot" title="Selected State Median Price Per Square Foot">
    <ReferenceLine x='2020-03-11' label="Start Covid Pandemic" hideValue=true/>
    <ReferenceLine x='2023-05-05' label="End Covid Pandemic" hideValue=true/>
</LineChart>




```sql homes_sold_per_state
    SELECT * FROM homes_sold_per_state
    WHERE state LIKE '${inputs.state.value}'
    AND property_type like '${inputs.Property_Types}'
```

<!-- <LineChart 
    data={homes_sold_per_state
    }  
    x=period_end
    y=homes_sold
    title="Selected States Homes Sold"
/> -->


<LineChart data={homes_sold_per_state} x=period_end y=homes_sold yAxisTitle="Median Homes Sold" title="Selected State Homes Sold Per Month">
    <ReferenceLine x='2020-03-11' label="Start Covid Pandemic" hideValue=true/>
    <ReferenceLine x='2023-05-05' label="End Covid Pandemic" hideValue=true/>
</LineChart>


```sql scatter_chart
SELECT * FROM combined_price_homes_sold
WHERE property_type like '${inputs.Property_Types}'
AND state not in('United States', 'Columbia')
```

<ScatterPlot 
    data={scatter_chart} 
    x=median_sale_price
    y=homes_sold
    series=state
    xAxisTitle=true 
    yAxisTitle=true
    title="Median Sale Price vs Homes Sold"
/>

```sql map
SELECT * FROM combined_price_homes_sold
WHERE property_type like '${inputs.Property_Types}'
```

<USMap
    data={map}
    state=state
    value=median_sale_price
    colorScale=bluegreen
    title="Median Sale Price Per State Map"
/>