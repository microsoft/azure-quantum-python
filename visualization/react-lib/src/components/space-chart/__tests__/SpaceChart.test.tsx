import  React from "react";
import { default as SpaceChart, SpaceChartProps } from "../SpaceChart";
import * as d3 from "d3";
import Adapter from 'enzyme-adapter-react-15';
import { shallow } from "enzyme";

describe("IconActionButton tests", () => {
    if(1==1){
            console.log("d");
    }
    it("Verify IconActionButton", () => {
        const props: SpaceChartProps = {
            physicalQubitsAlgorithm: 10,
            physicalQubitsTFactory: 32,
            width: 1000,
            height: 1000,
            innerRadius: 125,
            outerRadius: 200
        };
       const component = shallow(<SpaceChart {...props}/>);
        expect(component).toMatchSnapshot("IconActionButton");
    });
});

