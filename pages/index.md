---
title: Redfin Real Estate Report
---

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
    title="Select a Property Type"
>
    <!-- <ButtonGroupItem valueLabel="All Categories" value="%" default /> -->
    <!-- <ButtonGroupItem valueLabel=Townhouse default /> -->
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
    title="20 Highest Median Sale Price By Property Type"
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
    title="20 Lowest Median Sale Price By Property Type"
/>

```sql median_sale_price_by_state
    SELECT * FROM median_sale_price_per_state
    WHERE state in ${inputs.state.value}
    AND property_type like '${inputs.Property_Types}'
```


<LineChart data={median_sale_price_by_state} x=period_end y=median_sale_price, yAxisTitle="Median Sale Price", title='Selected State Median Sale Price'>
    <ReferenceLine x='2020-03-11' label="Start Covid Pandemic" hideValue=true/>
    <ReferenceLine x='2023-05-05' label="End Covid Pandemic" hideValue=true/>
</LineChart>


```sql median_ppsf_per_state
    SELECT * FROM median_ppsf_per_state
    WHERE state in ${inputs.state.value}
    AND property_type like '${inputs.Property_Types}'
```

<LineChart 
    data={median_ppsf_per_state
    }  
    x=period_end
    y=median_ppsf
    title="Selected States Median Price Per Square Foot"
/>


```sql homes_sold_per_state
    SELECT * FROM homes_sold_per_state
    WHERE state in ${inputs.state.value}
    AND property_type like '${inputs.Property_Types}'
```

<LineChart 
    data={homes_sold_per_state
    }  
    x=period_end
    y=homes_sold
    title="Selected States Homes Sold"
/>

```sql scatter_chart
SELECT * FROM combined_price_homes_sold
WHERE property_type like '${inputs.Property_Types}'
AND state not in('United States', 'Columbia')
```

<ScatterPlot 
    data={scatter_chart} 
    x=median_sale_price
    y=homes_sold
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