import React from 'react';
import '../css/Dashboard.css';

const Dashboard = () => {
    return (
        <div className="Dashboard">
            <div className="DashboardItem Word">
                <div className="DashboardItemTitle">
                    최근 일주일 핵심 단어
                </div>
                <div className="DashboardItemContent">
                    코로나, 정부, 국민
                </div>
            </div>
            <div className="DashboardItem Count">
                <div className="DashboardItemTitle">
                    최근 일주일 청원 개수
                </div>
                <div className="DashboardItemContent">
                    00 개
                </div>
            </div>
        </div>
    )
}

export default Dashboard;